from pwn import*
from tqdm import tqdm
import json
context.log_level = 'info'

r = remote("socket.cryptohack.org", 13423)
block_size = 16


def get_ct():
    r.sendline(json.dumps({"option": "encrypt"}).encode())
    res = json.loads(r.recvline().decode())["ct"]
    
    return res

def oracle(ct, k = 20):
    true = 0
    false = 0
    for _ in range(k):
        r.sendline(json.dumps({"option": "unpad", "ct": ct.hex()}).encode())
        res = json.loads(r.recvline().decode())["result"]
        
        if res == False:
            false += 1
        else:
            true += 1
            
    if false > true:
        return 1
    else:
        return 0
    
def count_iv_block(iv, pad_val):
    charset = b'1234567890abcdef'
    x = iv[-pad_val]
    return sorted(set([x ^ c ^ pad_val for c in charset]))


def solve_pt_block(block, iv_bytes):
    zeroing_iv = [0] * block_size
    
    for pad_val in tqdm(range(1, block_size + 1)):
        padding_iv = [pad_val ^ b for b in zeroing_iv]
        iv_block = count_iv_block(iv_bytes, pad_val)
        
        for c in iv_block:
            padding_iv[-pad_val] = c
            iv = bytes(padding_iv)
            if oracle(iv + block):
                if pad_val == 1:
                    padding_iv[-2] ^= 1
                    iv = bytes(padding_iv)
                    if not oracle(iv + block):
                        continue
                break
        
        else:
            raise Exception('[*] Invalid value!')

        zeroing_iv[-pad_val] = c ^ pad_val
        
    return zeroing_iv


def AES_CBC_Attack_Full(msg):

    blocks = [msg[i:i+block_size] for i in range(0, len(msg), 16)]
    iv = blocks[0]
    result = b''

    for block in blocks[1:]:
        dec = solve_pt_block(block, iv)
        pt = bytes([iv_bytes ^ dec_bytes for iv_bytes, dec_bytes in zip(iv, dec)])
        result += pt
        iv = block
        print('[*] Solve complete!')

    return result


r.recvline()
msg = bytes.fromhex(get_ct())
print(msg.hex(), len(msg))
pw = AES_CBC_Attack_Full(msg).decode()
assert len(pw) == 32
r.sendline(json.dumps({"option": "check", "message": pw}).encode())
print(r.recvall(timeout=2))

