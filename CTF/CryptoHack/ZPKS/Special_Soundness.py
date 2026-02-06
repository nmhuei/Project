from Crypto.Util.number import *
from pwn import*
import json, random
context.log_level = 'debug'

p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2

rem = remote("socket.cryptohack.org", 13426)
rem.recvline()

res= json.loads(rem.recvline().decode())
a = res["a"]
y = res["y"]

e = random.randint(0,q)
rem.sendline(json.dumps({"e": e}).encode())
z = json.loads(rem.recvline().decode())["z"]

res= json.loads(rem.recvline().decode())
a2 = res["a2"]
y = res["y"]

e2 = random.randint(0,q)
rem.sendline(json.dumps({"e": e2}).encode())
z2 = json.loads(rem.recvline().decode())["z2"]

flag = ((z -z2)*inverse(e - e2, q)) % q
print(long_to_bytes(flag))