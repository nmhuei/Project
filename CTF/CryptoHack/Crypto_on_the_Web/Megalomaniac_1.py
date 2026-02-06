from pwn import *
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import json, binascii
context.log_level = "DEBUG"

HOST, PORT = "socket.cryptohack.org", 13408  # hoặc theo đề
r = remote(HOST, PORT)

# 1) Nhận "material" in ra ở màn hình đầu (server gửi)
banner = r.recvuntil(b"}\n").decode()
j = json.loads(banner.splitlines()[-1])  # dòng JSON cuối cùng

n, e = j["share_key_pub"][0], j["share_key_pub"][1]
share_key_enc = bytes.fromhex(j["share_key_enc"])
master_key_enc = bytes.fromhex(j["master_key_enc"])

def mutate_share_key_enc(ct: bytes) -> bytes:
    blocks = [bytearray(ct[i:i+16]) for i in range(0, len(ct), 16)]
    # sửa block #40 (đánh số 1..41) => index 39
    blocks[39][0] ^= 1  # flip 1 bit là đủ
    return b"".join(blocks)

mut_ct = mutate_share_key_enc(share_key_enc)

def rsa_enc_raw(m: int) -> bytes:
    c = pow(m, e, n)
    # gửi dạng bytes big-endian tối thiểu
    return long_to_bytes(c)

def oracle_lt_q(m: int) -> bool:
    # 1) yêu cầu server chuyển sang LOGIN
    r.sendline(json.dumps({"action": "wait_login"}).encode())
    line = r.recvline().decode()
    # line chứa {"auth_key_hashed": ...}

    # 2) gửi thử thách với 3 trường đầy đủ
    payload = {
        "action": "send_challenge",
        "SID_enc": rsa_enc_raw(m).hex(),
        "share_key_enc": mut_ct.hex(),
        "master_key_enc": master_key_enc.hex(),
    }
    r.sendline(json.dumps(payload).encode())
    ans = json.loads(r.recvline().decode())

    if "SID" not in ans:
        # debug khi gặp lỗi
        print("[!] Server error:", ans)
        return False

    sid = bytes.fromhex(ans["SID"])
    m_bytes = long_to_bytes(m)
    expected_prefix = m_bytes[:-16] if len(m_bytes) > 16 else b""
    return sid == expected_prefix


# 2) Binary search tìm q
lo, hi = 1 << 1023, (1 << 1024) - 1
while lo < hi:
    mid = (lo + hi) // 2
    if oracle_lt_q(mid):
        lo = mid + 1    # m < q ⇒ q lớn hơn mid
    else:
        hi = mid
q = lo
p = n // q

# 3) Lấy encrypted_flag và giải
r.sendline(json.dumps({"action": "get_encrypted_flag"}).encode())
enc_flag_hex = json.loads(r.recvline().decode())["encrypted_flag"]
enc_flag = bytes.fromhex(enc_flag_hex)

secret = SHA256.new(long_to_bytes(p) + long_to_bytes(q)).digest()
flag = AES.new(secret, AES.MODE_ECB).decrypt(enc_flag)
# rồi PKCS#7 unpad → in flag
