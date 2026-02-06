import requests
from Crypto.Util.strxor import strxor

def encrypt():
    r = requests.get("https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/")
    r.raise_for_status()
    return r.json()["ciphertext"]

def decrypt(cipher):
    r = requests.get("https://aes.cryptohack.org/ecbcbcwtf/decrypt/" + cipher + "/")
    r.raise_for_status()
    return r.json()["plaintext"]


data = encrypt()
iv = data[:32]
blocks_ciphertext = [data[i:i+32] for i in range(32,len(data),32)]


for i, cipher in enumerate(blocks_ciphertext):
    plain_xor = decrypt(cipher)
    plain = strxor(bytes.fromhex(plain_xor), bytes.fromhex(iv))
    print(plain.decode(errors="ignore"), end='')
    iv = cipher

