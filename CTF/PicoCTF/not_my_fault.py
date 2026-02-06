import hashlib, random, string, gmpy2
from tqdm import tqdm
from pwn import *
context.log_level = 'debug'

r = remote('mercury.picoctf.net', '47414')
res = r.recvline().decode()


vals1 = res.split('"')[1]
vals2 = res.split()[-1]
print(vals1)
print(vals2)

while True:
    suffix = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    candidate = vals1 + suffix
    h = hashlib.md5(candidate.encode()).hexdigest()
    if h.endswith(vals2):
        print("[*] MD5 PoW Successfull:", candidate)
        print("[*] Hash:", h)
        break
# Send user_input    
r.sendline(candidate.encode())

# Recv public modulus
res = r.recvline().strip().decode()
N = int(res.split()[-1])

# Recv clue
res = r.recvline().strip().decode()
e = int(res.split()[-1])

# Calculate ans
m = 7516789928765
for d_p in tqdm(range(1, 2**20)):
    p = gmpy2.gcd(m - pow(m, e*d_p, N), N)
    if p > 1:
        break

q = N // p
ans = p + q

# Send ans and catch flag
r.sendline(str(ans).encode())

r.recvall(timeout=2)