from Crypto.Util.number import *
import random

def generate_basis(n):
    basis = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        if basis[i]:
            basis[i*i::2*i] = [False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3, n, 2) if basis[i]]

def miller_rabin(n, b):
    basis = generate_basis(b)
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for bb in basis:
        x = pow(bb, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# thử sinh pseudoprime nhỏ
def find_pseudoprime(bits=64):
    while True:
        p1 = getPrime(bits//2)
        p2 = getPrime(bits//2)
        n = p1 * p2   
        if miller_rabin(n, 64):
            return n

print(find_pseudoprime(64))

