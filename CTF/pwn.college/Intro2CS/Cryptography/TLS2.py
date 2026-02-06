#!/usr/bin/env python3
import sys
import base64
import json

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from pwn import *
import random

context.log_level = 'debug'

proc = process('/challenge/run')

def recv_info(s: bytes) -> str:
    proc.recvuntil(s)
    return proc.recvline().decode().strip()

# Get p, g, root_key_d, root_certificate, root_certificate_signature, name, A
p = int(recv_info(b'p:'), 16)
g = int(recv_info(b'g:'), 16)
root_key_d = int(recv_info(b'root key d:'), 16)
root_certificate = base64.b64decode(recv_info(b"root certificate (b64):").encode())
root_certificate = json.loads(root_certificate.decode())
_ = base64.b64decode(recv_info(b'root certificate signature (b64):').encode())  # ignore
name = recv_info(b"name:")
A = int(recv_info(b'A:'), 16)

# Enter input
# use a large private exponent so B > 2**1024
b = random.getrandbits(2048)
B = pow(g, b, p)
proc.sendlineafter(b'B:', hex(B)[2:].encode())

# derive AES key exactly as server: s.to_bytes(256, "little")
s = pow(A, b, p)
s_bytes = s.to_bytes(256, "little")
key = SHA256.new(s_bytes).digest()[:16]
iv = b"\x00" * 16
cipher_encrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
cipher_decrypt = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
bs = AES.block_size

# Generate user info
user_key = RSA.generate(1024)
user_certificate = {
    "name": name.strip(),
    "key": {
        "e": int(user_key.e),
        "n": int(user_key.n),
    },
    "signer": "root",
}
user_certificate_data = json.dumps(user_certificate).encode()

# user_certificate_signature: sign hash with root_key_d; use little-endian and 256 bytes
user_certificate_hash = SHA256.new(user_certificate_data).digest()
root_n = int(root_certificate["key"]["n"])
user_certificate_sig_int = pow(int.from_bytes(user_certificate_hash, "little"), root_key_d, root_n)
user_certificate_signature = user_certificate_sig_int.to_bytes(256, "little")

# user_signature: sign H(name||A||B) with user's private key; produce 256-byte little-endian
user_signature_data = (
    name.encode().ljust(256, b"\0")[:256] +
    A.to_bytes(256, "little") +
    B.to_bytes(256, "little")
)
user_signature_hash = SHA256.new(user_signature_data).digest()
user_sig_int = pow(int.from_bytes(user_signature_hash, "little"), int(user_key.d), int(user_key.n))
user_signature = user_sig_int.to_bytes(256, "little")

# Encrypt user info (pad -> AES-CBC -> base64)
user_certificate_data_enc = cipher_encrypt.encrypt(pad(user_certificate_data, bs))
user_certificate_signature_enc = cipher_encrypt.encrypt(pad(user_certificate_signature, bs))
user_signature_enc = cipher_encrypt.encrypt(pad(user_signature, bs))

user_certificate_data_b64 = base64.b64encode(user_certificate_data_enc)
user_certificate_signature_b64 = base64.b64encode(user_certificate_signature_enc)
user_signature_b64 = base64.b64encode(user_signature_enc)

# Send user info
proc.sendlineafter(b'user certificate (b64):', user_certificate_data_b64)
proc.sendlineafter(b"user certificate signature (b64):", user_certificate_signature_b64)
proc.sendlineafter(b"user signature (b64):", user_signature_b64)

# Get ciphertext and decrypt it to earn flag
secret_ciphertext_b64 = recv_info(b"secret ciphertext (b64):")
secret_ciphertext = base64.b64decode(secret_ciphertext_b64)
flag = unpad(cipher_decrypt.decrypt(secret_ciphertext), bs)

print('[*] Bypass Complete! Here is your flag:', flag.decode(errors="ignore"))
