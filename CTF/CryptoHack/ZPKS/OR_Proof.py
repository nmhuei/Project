from Crypto.Util.number import *
from hashlib import sha512
from pwn import*
import json, random
context.log_level = 'debug'

# Diffie-Hellman group (512 bits)
# p = 2*q + 1 where p,q are both prime, and 2 modulo p generates a group of order q
p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2

rem = remote("archive.cryptohack.org", 11840)
rem.recvline()
rem.recvline()

def send_param(x):
    rem.sendline(str(x).encode())
    
def recv_param():
    return int(rem.recvline().strip().decode().split()[-1])

# Correctness

# w,y for the relation `g^w = y mod p` we want to prove knowledge of
# w = random.randint(0,q)
# y = pow(g,w,p)
w0 = 0x5a0f15a6a725003c3f65238d5f8ae4641f6bf07ebf349705b7f1feda2c2b051475e33f6747f4c8dc13cd63b9dd9f0d0dd87e27307ef262ba68d21a238be00e83
y0 = 0x514c8f56336411e75d5fa8c5d30efccb825ada9f5bf3f6eb64b5045bacf6b8969690077c84bea95aab74c24131f900f83adf2bfe59b80c5a0d77e8a9601454e5
# w1 = REDACTED
y1 = 0x1ccda066cd9d99e0b3569699854db7c5cf8d0e0083c4af57d71bf520ea0386d67c4b8442476df42964e5ed627466db3da532f65a8ce8328ede1dd7b35b82ed617

assert (y0%p) >= 1 and (y1%p) >= 1
assert pow(y0, q, p) == 1 and pow(y1, q, p) == 1


r0 = 1
a0 = pow(g, r0)
r1 = 0
a1 = pow(g, r1)

assert (a0%p) >= 1 and (a1%p) >= 1
assert pow(a0, q, p) == 1 and pow(a1, q, p) == 1

send_param(a0)
send_param(a1)

s = recv_param()

e0 = s 
e1 = 0

z0 = (r0 + e0*w0) % q
z1 = 0

send_param(e0)
send_param(e1)
send_param(z0)
send_param(z1)


# specialSoundness

rem.recvline()

y0 = recv_param()
y1 = recv_param()
rem.recvline()

rem.recvline()
a0 = recv_param()
a1 = recv_param()
s = recv_param()
e0 = recv_param()
e1 = recv_param()
z0 = recv_param()
z1 = recv_param()

rem.recvline()
a0 = recv_param()
a1 = recv_param()
su = recv_param()
e0u = recv_param()
e1u = recv_param()
z0u = recv_param()
z1u = recv_param()

if pow(g, z0, p) == (a0 * pow(y0, e0, p)) % p:
    b = 0
else:
    b = 1
    
if b:
    a0,a1,e0,e1,z0,z1 = a1,a0,e1,e0,z1,z0
    
if b:
    e2 = e1u
    z2 = z1u
else:
    e2 = e0u
    z2 = z0u
    
w0 = ((z2 - z0)*inverse(e2 - e0, q)) % q

send_param(w0)
rem.recvline()

# SHVZK

rem.recvline()

y0 = recv_param()
y1 = recv_param()
s = recv_param()

def find(e, z, y, p=p):
    return (pow(g, z, p)*inverse(pow(y, e, p), p)) % p

e0 = random.randint(0, 2**511-1)
z0 = random.randint(0, 2**511-1)
a0 = find(e0, z0, y0)
e1 = s ^ e0
z1 = random.randint(0, 2**511-1)
a1 = find(e1, z1, y1)

send_param(a0)
send_param(a1)
send_param(e0)
send_param(e1)
send_param(z0)
send_param(z1)

rem.recvall(timeout=2)
