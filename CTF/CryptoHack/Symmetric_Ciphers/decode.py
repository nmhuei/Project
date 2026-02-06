from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from os import urandom

def xor_bytes(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

iv = urandom(16)
key = urandom(16)
msg = urandom(8).hex()  # 16 bytes, đúng cho AES block
print(msg.encode("ascii"))
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ct = cipher.encrypt(msg.encode("ascii"))
print("ct", (iv + ct).hex())
print("iv", iv.hex())
# Giải mã
dec_cipher = AES.new(key, AES.MODE_CBC, iv=iv)
pt = dec_cipher.decrypt(ct)
print("pt", pt.hex())

# XOR để check với IV
print("db", xor_bytes(pt, iv).hex())



pt = bytes.fromhex("33396238663564356631306233343265")
iv = bytes.fromhex("90a7cb2dbcef1ce2c603fc8e10cdd060")
db = xor_bytes(pt, iv).hex()
print([int(db[i:i+2], 16) for i in range(0, len(db), 2)])
iv = "90a7cb2dbcef1ce2c603fc8e10cdd060"
# Phân tích từng byte trong IV
charset = b'1234567890abcdef'.hex()

def count_iv_block(x):
    charset = b'1234567890abcdef'
    x = x[0]
    return sorted(set([x ^ c for c in charset]))

print(count_iv_block(bytes.fromhex("60")))
    