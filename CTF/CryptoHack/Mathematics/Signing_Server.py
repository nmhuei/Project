#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *
import json

HOST = "socket.cryptohack.org"
PORT = 13374

r = remote(HOST, PORT)

# đọc bỏ dòng chào đầu tiên (không phải JSON)
print(r.recvline().decode())

# B1: lấy public key
payload = {"option": "get_pubkey"}
r.sendline(json.dumps(payload).encode())
res = json.loads(r.recvline().decode())   # dùng loads để parse string JSON

n = int(res["N"], 16)
e = int(res["e"], 16)
print("N =", n)
print("e =", e)

# B2: lấy secret (c = m^e mod N)
payload = {"option": "get_secret"}
r.sendline(json.dumps(payload).encode())
res = json.loads(r.recvline().decode())
secret_ct = int(res["secret"], 16)
print("secret_ct =", secret_ct)

# B3: yêu cầu server ký một message thử (ví dụ "2")
msg = hex(secret_ct)
payload = {"option": "sign", "msg": msg}
r.sendline(json.dumps(payload).encode())
res = json.loads(r.recvline().decode())
sig = int(res["signature"], 16)
print("signature(2) =", sig)

r.close()

print(long_to_bytes(sig))