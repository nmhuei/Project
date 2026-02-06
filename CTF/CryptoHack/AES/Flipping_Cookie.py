import requests
from Crypto.Cipher import AES
import os
from datetime import datetime, timedelta
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from binascii import unhexlify, hexlify

def get_cookie():
    url = "https://aes.cryptohack.org/flipping_cookie/"
    r = requests.get(url + "get_cookie/")
    return r.json()["cookie"]

def check_admin(cookie, iv):
    url = "https://aes.cryptohack.org/flipping_cookie/"
    r = requests.get(url + "check_admin/" + cookie + "/" + iv + "/")
    return r.json()["flag"]
    
from binascii import unhexlify, hexlify

def flip_iv_to_admin(iv_hex):
    iv = bytearray(unhexlify(iv_hex))
    orig = b"admin=False;expiry="[:16]
    want = b"admin=True;expiry="[:16]   
    mask = bytes(o ^ w for o, w in zip(orig, want))
    for i, m in enumerate(mask):
        iv[i] ^= m
    return hexlify(iv).decode()



expires_at = (datetime.today() + timedelta(days=1)).strftime("%s")    
cookie = f"admin=True;expiry={expires_at}".encode()

data = get_cookie()
iv_hex = data[:32]
cookie = data[32:]
iv_prime_hex = flip_iv_to_admin(iv_hex)

res = check_admin(cookie, iv_prime_hex)

print(res)