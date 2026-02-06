import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import *
from sage.all import*

p = 1331169830894825846283645180581
a = -35
b = 98
E = EllipticCurve(GF(p), [a,b])

G = E(479691812266187139164535778017, 568535594075310466177352868412)
A = E(1110072782478160369250829345256, 800079550745409318906383650948)
B = E(1290982289093010194550717223760, 762857612860564354370535420319)
Encrypted_flag = {'iv': 'eac58c26203c04f68d63dc2c58d79aca', 'encrypted_flag': 'bb9ecbd3662d0671fd222ccb07e27b5500f304e3621a6f8e9c815bc8e4e6ee6ebc718ce9ca115cb4e41acb90dbcabb0d'}
iv = Encrypted_flag["iv"]
encrypted_flag = Encrypted_flag["encrypted_flag"]
iv = bytes.fromhex(iv)
encrypted_flag = bytes.fromhex(encrypted_flag)

# n_a = A.log(G)
n_a = 29618469991922269
print(n_a)

S = n_a * B
shared_secret = S.xy()[0]

sha1 = hashlib.sha1()
sha1.update(str(shared_secret).encode('ascii'))
key = sha1.digest()[:16]

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = cipher.decrypt(encrypted_flag)

print(unpad(plaintext, 16))

