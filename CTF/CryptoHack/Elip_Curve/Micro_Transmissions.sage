import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import *
from sage.all import*

def decrypt_flag(secret, iv, encrypted_flag):
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(encrypted_flag)

    try:
        print(unpad(plaintext, 16))
    except ValueError as e:
        print(e)


p = 99061670249353652702595159229088680425828208953931838069069584252923270946291
a = 1
b = 4
E = EllipticCurve(GF(p), [a, b])

G = E(43190960452218023575787899214023014938926631792651638044680168600989609069200, 20971936269255296908588589778128791635639992476076894152303569022736123671173)

Ax = 87360200456784002948566700858113190957688355783112995047798140117594305287669
Bx = 6082896373499126624029343293750138460137531774473450341235217699497602895121
data = {'iv': 'ceb34a8c174d77136455971f08641cc5', 'encrypted_flag': 'b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453'}
iv = bytes.fromhex(data['iv'])
encrypted_flag = bytes.fromhex(data['encrypted_flag'])

A = - E.lift_x(Ax)
B = E.lift_x(Bx)

order = G.order()
print(factor(order))

def find_n(P, Q):
    fac = list(factor(P.order()))
    moduli = []
    remainders = []
    for i in fac[0:-2]:
        P0 = P*ZZ(P.order()/(i[0]**i[1]))
        Q0 = Q*ZZ(P.order()/(i[0]**i[1]))
        moduli.append(i[0]**i[1])
        remainders.append(discrete_log(Q0,P0, operation = '+'))

    return crt(remainders,moduli)

nA = find_n(G, A)
print(nA)

S = nA * B
secret = S.xy()[0]

decrypt_flag(secret, iv, encrypted_flag)

