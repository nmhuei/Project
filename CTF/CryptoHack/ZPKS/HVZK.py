from Crypto.Util.number import *
from pwn import*
import json, random
context.log_level = 'debug'

p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2

rem = remote("socket.cryptohack.org", 13427)
rem.recvline()

res= json.loads(rem.recvline().decode())
e = res["e"]
y = res["y"]

def check(z, a):
    
    if (a%p) < 1 or pow(a, q, p) != 1:
        return 0

    return 1


while True:
    z = random.randint(0, 2**511)
    a = (pow(g, z, p)*inverse(pow(y, e, p), p)) % p
    if check(z, a):
        break

rem.sendline(json.dumps({"a": a, "z": z}).encode())
res = rem.recvline()

