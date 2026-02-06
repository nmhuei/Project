from Crypto.Cipher import AES
from Crypto.Util.Padding import *
from Crypto.Random import get_random_bytes
from pwn import*
from Crypto.Util.number import *
context.log_level = 'info'


def oracle(block):
    proc.sendline('TASK: ' + block.hex())
    res = proc.recvline().decode().strip()
    if 'Error' in res:
        return False

    return True
        

def solve_pt_block(block):
    zeroing_iv = [0] * block_size
    
    for pad_val in range(1, block_size + 1):
        padding_iv = [pad_val ^ b for b in zeroing_iv]

        for c in range(256):
            padding_iv[-pad_val] = c
            iv = bytes(padding_iv)
            if oracle(iv + block) == 1:
                if pad_val == 1:
                    padding_iv[-2] ^= 1
                    ic = bytes(padding_iv)
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

    for block in blocks:
        dec = solve_pt_block(block)
        pt = bytes([iv_bytes ^ dec_bytes for iv_bytes, dec_bytes in zip(iv, dec)])
        result += pt
        iv = block
        print('[*] Solve complete!')

    return result


block_size = 16
proc = process('/challenge/worker')

plaintext = pad(b"please give me the flag, kind worker process!", block_size)
plaintext_blocks = [plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]
data_hex = "00" * 160
data = bytes.fromhex(data_hex)

blocks = [data[i:i+block_size] for i in range(0, len(data), 16)]

for i in range(3, 0, -1):
    block = blocks[i]
    dec = solve_pt_block(block)
    iv = blocks[i-1]
    pt = plaintext_blocks[i-1]
    blocks[i-1] = bytes([dec_bytes ^ pt_bytes for dec_bytes, pt_bytes in zip(dec, pt)])

payload = ''.join(block.hex() for block in blocks[:4])
print(payload)
proc.sendline('TASK: ' + payload)
print(proc.recvall(timeout=2))