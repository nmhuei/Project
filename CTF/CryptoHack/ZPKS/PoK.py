from pwn import *
import json, random
context.log_level = 'debug'

rem = remote("socket.cryptohack.org", 13425)
rem.recvline()

# Diffie-Hellman group (512 bits)
# p = 2*q + 1 where p,q are both prime, and 2 modulo p generates a group of order q
p = 0x1ed344181da88cae8dc37a08feae447ba3da7f788d271953299e5f093df7aaca987c9f653ed7e43bad576cc5d22290f61f32680736be4144642f8bea6f5bf55ef
q = 0xf69a20c0ed4465746e1bd047f57223dd1ed3fbc46938ca994cf2f849efbd5654c3e4fb29f6bf21dd6abb662e911487b0f9934039b5f20a23217c5f537adfaaf7
g = 2


# w,y for the relation `g^w = y mod P` we want to prove knowledge of
# w = random.randint(0,q)
# y = pow(g,w,P)
w = 0x5a0f15a6a725003c3f65238d5f8ae4641f6bf07ebf349705b7f1feda2c2b051475e33f6747f4c8dc13cd63b9dd9f0d0dd87e27307ef262ba68d21a238be00e83
y = 0x514c8f56336411e75d5fa8c5d30efccb825ada9f5bf3f6eb64b5045bacf6b8969690077c84bea95aab74c24131f900f83adf2bfe59b80c5a0d77e8a9601454e5

r = random.getrandbits(128)
a = pow(g, r, p)

payload = {
    "a": a,
}
rem.sendline(json.dumps(payload).encode())
res = json.loads(rem.recvline().decode())
e = res["e"]

z = (r + e*w) % q

payload = {
    "z": z,
}
rem.sendline(json.dumps(payload).encode())
res = json.loads(rem.recvline().decode())
try:
    flag = res["flag"]
    print(flag)
    
except:
    print(res["error"])