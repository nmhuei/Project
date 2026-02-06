import base64
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *


r = remote("archive.cryptohack.org", 1024)

def auth(hash):
    r.recv()
    r.sendline(b'auth')
    pbox = r.recvline().decode().split()[1]
    salt = base64.b64decode(r.recvline().decode().split()[1])
    r.recv()
    r.sendline(hash)
    return pbox, salt
    
def spy(pbox, salt):
    r.recv()
    r.sendline(b'spy')
    r.sendline(pbox)
    r.sendline(salt)
    return r.recvline().decode().split()[-1]

