from Crypto.PublicKey import RSA
import requests, jwt

url = "https://web.cryptohack.org/rsa-or-hmac/"

def get_pubkey():
    res = requests.get(url + 'get_pubkey/')
    data = res.json()
    return data['pubkey']   # PEM string

# Lấy public key PEM
pubkey_pem = get_pubkey()
with open("key.pub", "w") as f:
    f.write(pubkey_pem)
    
# Parse thử để tham khảo modulus / exponent
key = RSA.import_key(pubkey_pem)
print("[+] n =", key.n)
print("[+] e =", key.e)

import hmac, hashlib, base64, json

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

header = {"alg": "HS256", "typ": "JWT"}
payload = {"username": "huei", "admin": True}

header_b64 = b64url(json.dumps(header, separators=(',',':')).encode())
payload_b64 = b64url(json.dumps(payload, separators=(',',':')).encode())

msg = f"{header_b64}.{payload_b64}".encode()

secret = pubkey_pem.encode()
sig = hmac.new(secret, msg, hashlib.sha256).digest()
sig_b64 = b64url(sig)

token = f"{header_b64}.{payload_b64}.{sig_b64}"
print("[+] Forged token:", token)
