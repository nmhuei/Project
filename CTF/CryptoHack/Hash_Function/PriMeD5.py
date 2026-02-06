from Crypto.Util.number import *
import os

# mở rộng ~ thành /home/<username>/
path1 = os.path.expanduser("~/hashclash/CTF/collision1.bin")
path2 = os.path.expanduser("~/hashclash/CTF/collision2.bin")

with open(path1, "rb") as f:
    data1 = f.read()

with open(path2, "rb") as f:
    data2 = f.read()

n1 = bytes_to_long(data1)
n2 = bytes_to_long(data2)

print(n1)
print(n2)

if isPrime(n1) or isPrime(n2):
    print("pass ✅")
else:
    print("not prime ❌")
