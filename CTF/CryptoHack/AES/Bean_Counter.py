from binascii import unhexlify
import requests

def decode(cipher_hex: str, out_path: str = "bean_flag.png") -> bytes:
    """
    Giải mã 'bean_counter' khi counter không tăng (keystream lặp lại mỗi block).
    - cipher_hex: chuỗi hex của ciphertext trả về từ /bean_counter/encrypt/
    - out_path: đường dẫn file PNG giải mã
    Trả về: bytes plaintext
    """
    # 16 byte đầu chuẩn của PNG: 8-byte signature + length(0x0000000D) + 'IHDR'
    png_header16 = bytes.fromhex("89504e470d0a1a0a0000000d49484452")

    ct = unhexlify(cipher_hex)
    if len(ct) < 16:
        raise ValueError("Ciphertext quá ngắn.")

    # Khôi phục keystream = C0 XOR P0 (với P0 là header PNG)
    ks = bytes(c ^ p for c, p in zip(ct[:16], png_header16))

    # Giải mã: mỗi block XOR cùng một keystream
    pt = bytearray()
    for i in range(0, len(ct), 16):
        block = ct[i:i+16]
        # cắt keystream nếu là block cuối không đủ 16 byte
        pt_block = bytes(b ^ ks[j] for j, b in enumerate(block))
        pt.extend(pt_block)

    # Lưu ra file
    with open(out_path, "wb") as f:
        f.write(pt)
    return bytes(pt)

# Ví dụ dùng:
# decrypted = decode(cipher_hex_from_api, "bean_flag.png")
# print("Done, saved to bean_flag.png")
def encrypt():
    r = requests.get(f"https://aes.cryptohack.org/bean_counter/encrypt/")
    return r.json()["encrypted"]

data = encrypt()
decrypted = decode(data, "beancounter.png")