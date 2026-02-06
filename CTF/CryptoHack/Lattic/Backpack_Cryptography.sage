from sage.all import *
from Crypto.Util.number import long_to_bytes
import output  # hoặc bạn paste public_key, encrypted vào đây

A = list(map(ZZ, output.public_key))
T = ZZ(output.encrypted_flag)
n = len(A)

# 1. Tạo ma trận cơ sở
M = Matrix(ZZ, n+1, n+1)
for i in range(n):
    M[i, i] = 1
    M[i, n] = A[i]
M[n, n] = -T

# 2. Chạy LLL
R = M.LLL()

# 3. Tìm vector ngắn
for v in R:
    if v[-1] == 0 and all(abs(x) <= 1 for x in v[:-1]):
        bits = [int(x) for x in v[:-1]]
        break
else:
    # fallback: tìm vector gần 0
    v = min(R, key=lambda x: x.norm())
    bits = [1 if x < 0 else 0 for x in v[:-1]]

# 4. Chuyển bit về chuỗi bytes (LSB-first)
val = 0
for i, b in enumerate(bits):
    val |= (b << i)

flag = long_to_bytes(val)
print(flag)
