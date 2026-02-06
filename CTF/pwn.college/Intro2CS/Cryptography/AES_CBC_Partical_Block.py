from Crypto.Cipher import AES
from Crypto.Util.Padding import *
from Crypto.Random import get_random_bytes
from pwn import*
from Crypto.Util.number import *
context.log_level = 'info'

proc = process('/challenge/worker')
proc.recvline()
data = bytes.fromhex("a042425c876c85cdd97d180cd5eef4e22baf822d007d639ae1ce6c5e09cb2496")
block_size = 16
iv = data[:16]
block = data[16:]

def oracle(block):
    proc.sendline('TASK: ' + block.hex())
    print('TASK: ' + block.hex())
    res = proc.recvline().decode().strip()
    print(res)
    if 'Error' in res:
        return False

    return True
        

def solve_pt_block(ct, block):
    zeroing_iv = [0] * block_size
    
    for pad_val in range(1, block_size + 1):
        print(f'[*] Solve iv[{17 - pad_val}]')
        padding_iv = [pad_val ^ b for b in zeroing_iv]
        
        for c in range(256):
            print(c)
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

dec = solve_pt_block(iv, block)
pw = bytes(iv_bytes ^ dec_bytes for iv_bytes, dec_bytes in zip(iv, dec))
print(pw)

    
            
