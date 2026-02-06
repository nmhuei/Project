from Crypto.Util.number import *
from Crypto.Util.Padding import *
from Crypto.Cipher import AES
import hashlib

p = 110791754886372871786646216601736686131457908663834453133932404548926481065303
G = 11
K = GF(p)
A = K(109790246752332785586117900442206937983841168568097606235725839233151034058387)
B = K(45290526009220141417047094490842138744068991614521518736097631206718264930032)

n = A.log(11)
shared_secret = B**n

def decrypt_flag(secret, iv, encrypted_flag):
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(encrypted_flag)

    try:
        print(unpad(plaintext, 16))
    except ValueError as e:
        print(e)

data = {'iv': '31068e75b880bece9686243fa4dc67d0', 'encrypted_flag': 'e2ef82f2cde7d44e9f9810b34acc885891dad8118c1d9a07801639be0629b186dc8a192529703b2c947c20c4fe5ff2c8'}
iv = bytes.fromhex(data['iv'])
encrypted_flag = bytes.fromhex(data['encrypted_flag'])

decrypt_flag(shared_secret, iv, encrypted_flag)