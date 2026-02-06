from Crypto.Cipher import AES
from Crypto.Util.number import*
import os
import math

BLOCK_SIZE = 16
UMAX = int(math.pow(256, BLOCK_SIZE))

def remove_line(s: bytes):
    idx = s.index(b'\n')   # tìm vị trí xuống dòng trong bytes
    return s[:idx+1], s[idx+1:]

def parse_header_ppm(f):
    data = f.read()
    header = b""   # giữ header dạng bytes

    for _ in range(3):  # PPM header có 3 dòng đầu
        header_i, data = remove_line(data)
        header += header_i

    return header, data

def aes_abc_decrypt(ct_abc):
    # Tách thành từng block 16 bytes
    blocks = [ct_abc[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE] for i in range(len(ct_abc)//BLOCK_SIZE)]
    
    
    # Đảo ngược phép cộng modulo UMAX
    for i in range(len(blocks) - 1, 0, -1):
        prev_blk = bytes_to_long(blocks[i-1])
        curr_blk = bytes_to_long(blocks[i])
        
        orig_blk = (curr_blk - prev_blk) % UMAX
        blocks[i] = long_to_bytes(orig_blk, BLOCK_SIZE)

    blocks = blocks[1:]

    # Ghép lại (plaintext đã được AES-ECB encrypt + pad)
    ct = b"".join(blocks)
    return ct
        
with open("body.enc.ppm", "rb") as f:
    header, data_encrypt = parse_header_ppm(f)

ct = aes_abc_decrypt(data_encrypt)



# Ghi lại ảnh
with open("flag_decrypted.ppm", "wb") as fw:
    fw.write(header)
    fw.write(ct)



