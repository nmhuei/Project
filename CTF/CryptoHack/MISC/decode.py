from Crypto.Util.number import *
from pwn import*
import json
context.log_level = 'debug'


my_1k_wallet_privkey = "8b09cfc4696b91a1cc43372ac66ca36556a41499b495f28cc7ab193e32eadd30"
r = remote("socket.cryptohack.org", 13384)
p = 2**521 - 1

data = json.loads(r.recvline().decode())
x, y = data["x"], data["y"]

r.recvline()
r.recvline()
r.recvline()
r.recvline()

r.sendline(json.dumps({"x": x, "y": "0x00000"}).encode())
data = json.loads(r.recvline().decode())
private = data["privkey"]

r.recvline()
r.recvline()

scamer = hex((-int(private, 16) + int(my_1k_wallet_privkey, 16)) * inverse(5, p) % p)
r.sendline(json.dumps({"x": 6, "y": scamer}).encode())
r.recvline()
r.recvline()

private_1M_wallet = hex((int(private, 16) + 5*int(y, 16)) % p) 
r.sendline(json.dumps({"privkey": private_1M_wallet}).encode())
r.recvall(timeout=2)