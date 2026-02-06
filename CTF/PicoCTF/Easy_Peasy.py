from pwn import*
import json, sys, binascii
context.log_level = "DEBUG"

HOST, POST = "mercury.picoctf.net", 64260

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

io = remote(HOST, POST)

welcome = io.recvuntil(b"This is the encrypted flag!\n")
flag_hex = io.recvline().strip().decode()
Lf = len(flag_hex) // 2

KEY_LEN = 50000
L1 = KEY_LEN - Lf
io.recvuntil(b"What data would you like to encrypt? ")
io.sendline(b"A" * L1)
io.recvuntil(b"Here ya go!\n")
ct1_hex = io.recvline().strip().decode()
key_tail = xor_bytes(bytes.fromhex(ct1_hex), b"\x41" * L1)

# 3) Bước 2: gửi 'A' * Lf để lấy key[0:Lf]
io.recvuntil(b"What data would you like to encrypt?")
io.sendline(b"A" * Lf)
io.recvuntil(b"Here ya go!\n")
ct2_hex = io.recvline().strip().decode()
key_head = xor_bytes(bytes.fromhex(ct2_hex), b"\x41" * Lf)

flag = xor_bytes(bytes.fromhex(flag_hex), key_head)
print("[FLAG]", flag.decode(errors="replace"))