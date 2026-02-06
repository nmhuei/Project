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

FLAG = b"crypto{????????????????????}"

# w,y for the relation `g^w = y mod P` we want to prove knowledge of
# w = random.randint(0,q)
# y = pow(g,w,P)
w = 0xdb968f9220c879b58b71c0b70d54ef73d31b1627868921dfc25f68b0b9495628b5a0ea35a80d6fd4f2f0e452116e125dc5e44508b1aaec89891dddf9a677ddc0
y = 0x1a1b551084ac43cc3ae2de2f89c6598a081f220010180e07eb62d0dee9c7502c1401d903018d9d7b06bff2d395c46795aa7cd8765df5ebe7414b072c8289170f0

rem = remote("socket.cryptohack.org", 13428)
rem.recvline()

y = json.loads(rem.recvline().decode())["y"]

r = random.randint(0, 2**511)
a = pow(g, r, p)
fiat_shamir_input = str(a).encode()
e = bytes_to_long(sha512(fiat_shamir_input).digest()) % 2**511

z = (r + e*w) % q

rem.sendline(json.dumps({"a": a, "z": z}))
rem.recvline()