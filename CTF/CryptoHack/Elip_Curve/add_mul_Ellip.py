from Crypto.Util.number import inverse
from Crypto.Cipher import AES
from hashlib import sha1

a = 497
b = 1768
p = 9739

assert (4*(a**3) + 27*(b**2)) % p != 0


def add2ellippoint(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # Nếu P và -Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None   # điểm vô cực O

    if P != Q:
        lam = ((y2 - y1) * inverse(x2 - x1, p)) % p
    else:
        lam = ((3 * x1 * x1 + a) * inverse(2*y1, p)) % p

    x3 = (lam*lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return [x3, y3]


def mul(n, P):
    R = None   # bắt đầu với O
    Q = P
    while n > 0:
        if n % 2 == 1:
            R = add2ellippoint(R, Q)
        Q = add2ellippoint(Q, Q)
        n //= 2
    return R

G = [1804, 5368]
x = 4726
sqr_y = (x ** 3 + a * x + b) % p
y = pow(sqr_y, (p+1)//4, p)
Qa = [x,y]
res = mul(6534, Qa)
print(res)