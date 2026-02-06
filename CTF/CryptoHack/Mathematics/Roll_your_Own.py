from Crypto.Util.number import *
from pwn import remote
import json


rn = remote('socket.cryptohack.org', 13403)
p = int(rn.recvline().decode().split('"')[1], 16)
rn.recvuntil(b':')
rn.send(json.dumps({'g': hex(p + 1), 'n': hex(p ** 2)}).encode())
key = int(rn.recvline().decode().split('"')[1], 16)
rn.recvuntil(b':')
x = (key - 1) // p
rn.send(json.dumps({'x': hex(x)}).encode())
print(json.loads(rn.recvline().decode())['flag'])