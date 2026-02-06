from Crypto.Util.number import*
from sympy.ntheory.modular import crt
import ast

with open("out.txt", "r") as f:
    N, ct = f.read().split()
    N = int(N, 16)
    ct = int(ct, 16)
    
with open("factors.txt", "r", encoding="utf-8") as f:
    content = f.read()
    p_list = ast.literal_eval(content)

p_list = p_list[:5]
    
e = 0x10001
d_list = [inverse(e, p-1) for p in p_list]
m_list = [pow(ct, d, p) for d, p in zip(d_list, p_list)]

flag, _ = crt(p_list, m_list)
print(long_to_bytes(flag))