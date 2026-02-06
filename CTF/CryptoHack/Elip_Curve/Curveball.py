#!/usr/bin/env python3
import json
from pwn import remote
from fastecdsa.point import Point
from fastecdsa.curve import P256

# target public key T (trusted www.bing.com trong challenge)
Tx = 0x3B827FF5E8EA151E6E51F8D0ABF08D90F571914A595891F9998A5BD49DFA3531
Ty = 0xAB61705C502CA0F7AA127DEC096B2BBDC9BD3B4281808B3740C320810888592A
T = Point(Tx, Ty, curve=P256)

n = P256.q

# Chọn d sao cho abs(d) != 1 (vd d = 2)
d = 2

# Nghịch đảo của d modulo n
inv_d = pow(d, -1, n)   # Python 3.8+: modular inverse

# Tính g = inv_d * T
g = inv_d * T   # scalar * Point -> Point

payload = {
    "private_key": d,              # số nhỏ, không bị chặn (abs(d) != 1)
    "host": "www.bing.com",        # trường host bất kỳ (server sẽ trả chính host từ trusted nếu có match)
    "curve": "secp256r1",
    "generator": [int(g.x), int(g.y)]
}

print("Payload being sent:")
print(json.dumps(payload, indent=2))

# Gửi payload tới server challenge (giống listener trong challenge)
r = remote("socket.cryptohack.org", 13382)
r.send(json.dumps(payload).encode())
res = r.recvall(timeout=5)
print("Response:")
print(res.decode())
