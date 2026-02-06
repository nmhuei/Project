#!/usr/bin/env python3
# pwn_decode.py
# Yêu cầu: pip install pwntools

from pwn import remote, Timeout
import re
import sys

HOST = "verbal-sleep.picoctf.net"
PORT = 58153
RECV_TIMEOUT = 5  # giây, chỉnh nếu cần

def decode_from_text(text):
    # Lấy tất cả các '0x..' theo thứ tự xuất hiện
    hexes = re.findall(r'0x[0-9A-Fa-f]{2}', text)
    return ''.join(chr(int(h, 16)) for h in hexes), hexes

def main():
    print(f"[+] Connecting to {HOST}:{PORT} ...")
    try:
        r = remote(HOST, PORT, timeout=RECV_TIMEOUT)
    except Exception as e:
        print("[-] Không kết nối được:", e, file=sys.stderr)
        return

    received_chunks = []
    try:
        # Thu thập tới khi server đóng kết nối hoặc timeout
        with timeout(RECV_TIMEOUT):
            while True:
                chunk = r.recv(timeout=1)
                if not chunk:
                    break
                # đảm bảo decode an toàn
                try:
                    received_chunks.append(chunk.decode('utf-8', errors='ignore'))
                except:
                    received_chunks.append(str(chunk))
    except Exception:
        # timeout hoặc server đóng kết nối
        pass

    # Đóng kết nối nếu vẫn còn
    try:
        r.close()
    except:
        pass

    full = ''.join(received_chunks)
    print("=== RAW RECEIVED ===")
    print(full)
    print("=== DECODING ===")
    flag, hexes = decode_from_text(full)
    if hexes:
        print("[*] Found bytes:", ' '.join(hexes))
        print("[*] Decoded flag / message:")
        print(flag)
    else:
        print("[-] Không tìm thấy chuỗi 0x.. nào trong dữ liệu nhận được.")

if __name__ == "__main__":
    main()
