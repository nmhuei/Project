from pwn import*
from tqdm import tqdm
import os
import random
context.log_level = 'warning'

def connection():
    r = remote("archive.cryptohack.org", 63222)
    r.recvline()
    
    indices = random.sample(range(2019), 2)  # chọn 2 phần tử khác nhau
    i1, i2 = indices
    
    r.sendline(str(i1).encode())
    r.sendline(str(i2).encode())
    print(i1, i2)
    numbers = []
    d = 0
    for i in range(2019):
        res = r.recvline().strip().decode()
        if res != "Nope!":
            numbers.append({"i": i, "r": res})
            
    if d == 0:
            r.close()
            return 0

    print(numbers)
    r.sendline(str(random.getrandbits(32)).encode())
    print(r.recvall(timeout=0.5))
    return 1

while True:
    k = connection()
    if k == 1:
        
        
        exit()
        
                        