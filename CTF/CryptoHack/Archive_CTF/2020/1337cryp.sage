import ast
from gmpy2 import jacobi
from Crypto.Util.number import long_to_bytes

# Đọc toàn bộ file
with open("out.txt", "r") as f:
    data = f.read()

# Tách các biến ra
lines = data.splitlines()
hint = int(lines[0].split("=", 1)[1].strip())
D = int(lines[1].split("=", 1)[1].strip())
n = int(lines[2].split("=", 1)[1].strip())

# Parse list c (có thể dài nhiều dòng)
c_text = "\n".join(lines[3:]).split("=", 1)[1].strip()
c = ast.literal_eval(c_text)   # list[int]

# get an approximation for p
F.<x> = ZZ[]
poly = x^2 - x*hint + D*D*sqrt(n)
d = poly.roots()
p_approx = int((d[0][0]/D)^2)

# compute the exact value of p
P.<x> = PolynomialRing(Zmod(n), implementation='NTL')
f = x + p_approx
d = f.small_roots(X=2**590, beta=0.4, epsilon=1/32)
p = p_approx + d[0]
assert is_prime(p)
print('[+] recovered p', p)

# get the flag
flag = ''.join('0' if kronecker(x, p) == -1 else '1' for x in c)
flag = long_to_bytes(int(flag, 2))
print('[*] flag:', flag.decode())