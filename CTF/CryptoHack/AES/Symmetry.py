import requests
from Crypto.Util.strxor import strxor
from binascii import unhexlify

BASE = "https://aes.cryptohack.org/symmetry/"

def encrypt_flag():
    r = requests.get(BASE + "encrypt_flag/")
    data = r.json()["ciphertext"]
    return data[:32], data[32:]  # iv_hex, cipher_hex

def encrypt(pt_hex, iv_hex):
    r = requests.get(BASE + "encrypt/" + pt_hex + "/" + iv_hex + "/")
    return r.json()["ciphertext"]

# Lấy IV và ciphertext flag
iv_hex, cipher_hex = encrypt_flag()
cipher_bytes = unhexlify(cipher_hex)

# Xin keystream có cùng độ dài
zeros = "00" * len(cipher_bytes)
keystream_hex = encrypt(zeros, iv_hex)
keystream = unhexlify(keystream_hex)

# Giải mã
plaintext = strxor(cipher_bytes, keystream)
print(plaintext)
