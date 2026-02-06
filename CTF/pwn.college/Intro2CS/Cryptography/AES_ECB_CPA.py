#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exploit cho challenge AES-ECB:
  - Option 1: encrypt chosen plaintext (Data?)
  - Option 2: encrypt part of flag (Index? Length?)
So sánh ciphertext của 2 option để dò flag byte-by-byte.

Usage:
  python3 decode.py
  python3 decode.py --bin ./challenge/run
  python3 decode.py --remote 1.2.3.4:1337
  python3 decode.py --prefix picoCTF{ --delay 0.01
  python3 decode.py --full-bytes   # thử toàn bộ 0..255 (risky if server dùng input() và decode)
"""
from pwn import *
import string
import sys
import time
import argparse

# Set log level ('debug' để xem mọi I/O)
context.log_level = 'info'

# ---------- Config mặc định ----------
DEFAULT_BIN = '/challenge/run'      # đường dẫn local binary/script
DEFAULT_PREFIX = b'pwn.college{'         # chỉnh nếu bạn biết prefix
# Xây charset mặc định: printable nhưng loại bỏ '\n' và '\r'
_printable = string.printable.replace('\n', '').replace('\r', '')
# ưu tiên các ký tự hay gặp trong flag
PRIORITY = '_}' + string.digits + string.ascii_lowercase + string.ascii_uppercase
# đưa các ký tự khác (punctuation, spaces...) sau
OTHER = ''.join(ch for ch in _printable if ch not in PRIORITY)
CHARSET_DEFAULT = (PRIORITY + OTHER).encode()

IO_TIMEOUT = 3.0
DELAY_DEFAULT = 0.005   # delay giữa các thử

# ---------- Kết nối ----------
def get_tube(args):
    if args.remote:
        host, port = args.remote.split(':')
        return remote(host, int(port), timeout=IO_TIMEOUT)
    else:
        return process(args.bin, timeout=IO_TIMEOUT)

# ---------- Giao tiếp với challenge ----------
def encrypt_pt(p, pt: bytes) -> str:
    """
    Gọi option 1: gửi plaintext (dùng sendline vì server dùng input()).
    Trả về hex string (không có newline).
    """
    p.sendlineafter(b'Choice? ', b'1')
    # pt là bytes; sendlineafter chấp nhận bytes và thêm newline
    p.sendlineafter(b'Data? ', pt)
    p.recvuntil(b'Result: ')
    return p.recvline(timeout=IO_TIMEOUT).strip().decode()

def encrypt_flag_part(p, index: int, length: int) -> str:
    """
    Gọi option 2: gửi index/length, nhận hex string ciphertext.
    """
    p.sendlineafter(b'Choice? ', b'2')
    p.sendlineafter(b'Index? ', str(index).encode())
    p.sendlineafter(b'Length? ', str(length).encode())
    p.recvuntil(b'Result: ')
    return p.recvline(timeout=IO_TIMEOUT).strip().decode()

# ---------- Brute logic ----------
def brute(args):
    p = get_tube(args)
    try:
        # xử lý charset & prefix
        if args.full_bytes:
            charset = bytes(range(0, 256))
        else:
            charset = args.charset if isinstance(args.charset, bytes) else args.charset.encode()

        flag = args.prefix if isinstance(args.prefix, bytes) else args.prefix.encode()
        print(f"[+] Start. Prefix: {flag!r}, charset length: {len(charset)}")

        while not flag.endswith(b'}'):
            found = None
            print(f"[+] Current flag: {flag.decode(errors='ignore')}")
            for c in charset:
                candidate = flag + bytes([c])
                try:
                    out_pt = encrypt_pt(p, candidate)
                    out_flag = encrypt_flag_part(p, 0, len(candidate))
                except EOFError:
                    print("[!] EOFError: connection closed unexpectedly.")
                    p.close()
                    return None
                except Exception as e:
                    print("[!] I/O error:", e)
                    p.close()
                    return None

                # So sánh hex strings
                if out_pt == out_flag:
                    try:
                        ch_repr = chr(c) if 32 <= c <= 126 else f"\\x{c:02x}"
                    except Exception:
                        ch_repr = f"\\x{c:02x}"
                    print(f"[+] Found next byte: {ch_repr}")
                    found = c
                    break

                time.sleep(args.delay)

            if found is None:
                print("[!] Không dò được ký tự tiếp theo. In debug:")
                try:
                    print("    last candidate (repr):", repr(candidate))
                    print("    last out_pt   :", out_pt)
                    print("    last out_flag :", out_flag)
                except NameError:
                    print("    (Chưa có thử nào thành công)")
                p.close()
                return None

            flag += bytes([found])

        print("[*] Flag recovered:", flag.decode(errors='ignore'))
        return flag.decode(errors='ignore')
    finally:
        try:
            p.close()
        except:
            pass

# ---------- CLI ----------
def build_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin', default=DEFAULT_BIN, help="Local binary path")
    ap.add_argument('--remote', default=None, help="Remote host:port")
    ap.add_argument('--prefix', default=DEFAULT_PREFIX.decode(), help="Initial prefix (string)")
    ap.add_argument('--charset', default=None, help="Custom charset string (no \\n or \\r).")
    ap.add_argument('--delay', type=float, default=DELAY_DEFAULT, help="Delay between tries (seconds).")
    ap.add_argument('--full-bytes', action='store_true', help="Try full byte range 0..255 (risky with Python input()).")
    return ap

def main():
    parser = build_parser()
    args = parser.parse_args()

    # charset xử lý
    if args.charset is None:
        args.charset = CHARSET_DEFAULT
    else:
        # đảm bảo loại newline/carriage return nếu user nhập thủ công
        s = args.charset.replace('\n', '').replace('\r', '')
        args.charset = s.encode()

    args.prefix = args.prefix.encode()
    # set global delay
    global DELAY_DEFAULT
    DELAY_DEFAULT = args.delay

    res = brute(args)
    if res:
        print("[+] Done:", res)
    else:
        print("[!] Exploit failed or stopped.")

if __name__ == '__main__':
    main()
