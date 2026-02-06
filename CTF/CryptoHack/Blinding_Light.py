from Crypto.Util.number import *
from pwn import *
import json


context.log_level = "debug"
HOST, POST = "socket.cryptohack.org", 13376
r = remote(HOST, POST)

def get_pubkey():
    payload = {"option": "get_pubkey"}
    r.sendline(json.dumps(payload).encode())
    res = json.loads(r.recvline().decode())
    return res["N"], res["e"]

def decrypt(msg):
    payload = {"option": "sign", "msg": msg}
    r.sendline(json.dumps(payload).encode())
    res = json.loads(r.recvline().decode())
    return res["signature"]

def verify(msg, sign):
    payload = {"option": "verify", "msg": msg,"signature": sign}
    r.sendline(json.dumps(payload).encode())
    res = json.loads(r.recvline().decode())
    return res["response"]


r.recvuntil("Watch out for the Blinding Light\n")

n, e = get_pubkey()
n = int(n, 16)
e = int(e, 16)
ADMIN_TOKEN = b"admin=True"
msg = bytes_to_long(ADMIN_TOKEN) * pow(2, e, n) % n
msg = hex(msg)[2:]
sign = hex(int(decrypt(msg), 16) * inverse(2, n) % n)[2:]
msg = ADMIN_TOKEN.hex()

flag = verify(msg, sign)

print(flag)




