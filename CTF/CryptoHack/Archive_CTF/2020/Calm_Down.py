import base64
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *

def orcale_ifValid(msg_long):
    msg_base64 = base64.b64encode(long_to_bytes(msg_long))
    msg_full = b'send ' + msg_base64
    proc.sendline(msg_full)
    data = proc.recvuntil(b'[cmd] ')
    result = data.replace(b'\n[cmd] ', b'')
    return (result == b'nice')

proc = remote("archive.cryptohack.org", 53580)

data = proc.recvuntil(b'[cmd] ')
proc.sendline(b'pkey')
data = proc.recvuntil(b'[cmd] ')
data = data.replace(b'[pkey] ', b'')
n_base64 = data.replace(b'\n[cmd] ', b'')

proc.sendline(b'read')
data = proc.recvuntil(b'[cmd] ')
data = data.replace(b'[shhh] ', b'')
c_base64 = data.replace(b'\n[cmd] ', b'')

n = bytes_to_long(base64.b64decode(n_base64))
e = 65537
c = bytes_to_long(base64.b64decode(c_base64))

s = 0x81
count = 2
while True:
    s += pow(16, count) * 15
    print(hex(s))
    c1 = pow(s, e, n) * c 
    valid = orcale_ifValid(c1)
    if not valid:
        break
    count += 1
    
times = 0
while True:
    if times < 15:
        s -= pow(16,count)
        print(hex(s))
        c1 = pow(s, e, n) * c
        if orcale_ifValid(c1):
            s += pow(16, count)
            times = 0
            count -= 1
            if count == 1:
                break
            
        else:
            times += 1
            
    else:
        times = 0
        count -= 1
        if count == 1:
            break
        
print(long_to_bytes(n // s))