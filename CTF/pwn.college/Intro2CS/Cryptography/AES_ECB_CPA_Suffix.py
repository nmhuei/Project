#!/usr/bin/env python3
# exploit_tail.py — brute-force flag from tail using chosen-plaintext vs tail oracle
from pwn import *
import string
import time

context.log_level = 'info'

# chỉnh nếu cần
BIN = '/challenge/run'   # hoặc '/challenge/run'
MAX_LEN = 120              # dừng sau MAX_LEN byte nếu chưa thấy pattern dừng
DELAY = 0.0                # khoảng nghỉ giữa thử (tăng nếu server rate-limit)

# charset ưu tiên
PRIORITY = '{_}' + string.digits + string.ascii_lowercase + string.ascii_uppercase
OTHER = ''.join(ch for ch in (string.printable.replace('\n','').replace('\r','')) if ch not in PRIORITY)
CHARSET = (PRIORITY + OTHER).encode()

# khởi tạo process (hoặc remote nếu bạn muốn)
p = process(BIN)

def encrypt_tail(length: int) -> str:
    p.sendlineafter(b'Choice? ', b'2')
    p.sendlineafter(b'Length? ', str(length).encode())
    p.recvuntil(b'Result: ')
    return p.recvline().strip().decode()

def encrypt_pt(pt: bytes) -> str:
    p.sendlineafter(b'Choice? ', b'1')
    p.sendlineafter(b'Data? ', pt)
    p.recvuntil(b'Result: ')
    return p.recvline().strip().decode()

def main():
    known = b''   # known_suffix (rightmost bytes)
    print("[*] Start brute from tail. Known suffix initially empty.")
    for k in range(1, MAX_LEN+1):
        target = encrypt_tail(k)   # ciphertext of flag[-k:]
        found = None
        print(f"[+] Looking for byte at position -{k} (making suffix length {k})")
        for c in CHARSET:
            cand = bytes([c]) + known   # try prepend a byte to the known suffix
            try:
                out = encrypt_pt(cand)
            except EOFError:
                print("[!] Connection closed unexpectedly"); return
            if out == target:
                known = cand
                # printable display
                try:
                    disp = known.decode()
                except:
                    disp = ''.join((chr(b) if 32<=b<127 else f"\\x{b:02x}") for b in known)
                print(f"[+] Found byte: {chr(c) if 32<=c<127 else f'\\x{c:02x}'}; suffix now: {disp}")
                found = c
                break
            time.sleep(DELAY)
        if found is None:
            print("[!] Không tìm thấy byte tiếp theo trong charset. Tạm dừng.")
            break
        # dừng nếu đã tìm thấy opening brace { khi đảo suffix => kiểm tra:
        # nếu reversed known startswith e.g. 'picoCTF{', ta có thể stop sớm
        rev = known[::-1]
        if rev.startswith(b'pwn.college{'):
            print("[*] Detected prefix 'picoCTF{' in reversed suffix — likely đã lấy đủ flag.")
            try:
                flag = rev.decode()
            except:
                flag = ''.join((chr(b) if 32<=b<127 else f"\\x{b:02x}") for b in rev)
            print("[*] Recovered flag:", flag)
            return
    # Nếu vòng kết thúc mà chưa detect pattern, in kết quả hiện tại (reversed)
    print("[*] Done loop. Current recovered suffix (right-to-left):", known)
    print("[*] Reversed (flag prefix..):", known[::-1].decode(errors='ignore'))

if __name__ == '__main__':
    try:
        main()
    finally:
        try:
            p.close()
        except:
            pass

