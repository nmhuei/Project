from pwn import *
import hashlib, json
from Crypto.Util.number import*
context.log_level = "DEBUG"

r = remote("socket.cryptohack.org", 13389)
r.recvuntil("Give me a document to store\n")

with open("collision1.bin", "rb") as f:
    key1 = bytes_to_long(f.read())
    key1 = hex(key1)[2:]
with open("collision2.bin", "rb") as f:
    key2 = bytes_to_long(f.read())
    key2 = hex(key2)[2:]

r.sendline(json.dumps({"document": key1}).encode())
r.recvline()
r.sendline(json.dumps({"document": key2}).encode())
r.recvall()

