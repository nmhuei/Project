import requests
import json

def encrypt(pt_hex, key_hex):
    url = f"http://aes.cryptohack.org/triple_des/encrypt/{key_hex}/{pt_hex}/"
    r = requests.get(url)
    try:
        enc = (json.loads(r.text))['ciphertext']
        return enc
    except:
        enc = (json.loads(r.text))
        return enc

def encrypt_flag(key_hex):
    url = f"http://aes.cryptohack.org/triple_des/encrypt_flag/{key_hex}/"
    r = requests.get(url)
    try:
        enc = (json.loads(r.text))['ciphertext']
        return enc
    except:
        enc = (json.loads(r.text))
        return enc

key = (b'\x00'*8 + b'\xff'*8).hex()
#print(key)
#print(len(key))
ct_flag = (encrypt_flag(key))

try:
    ct = encrypt(ct_flag,key)
    print(bytes.fromhex(ct))
except:
    print(ct)
    
#This challenge use the definition is weak key in DES