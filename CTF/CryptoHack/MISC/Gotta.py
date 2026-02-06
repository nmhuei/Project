from pwn import remote, context
import json
from Crypto.Util.strxor import strxor

context.log_level = "debug"   # bật log pwntools

HOST, PORT = "socket.cryptohack.org", 13372

def recv_json_line(r):
    line = r.recvline().strip()
    print("[DEBUG] raw line =", line)   # log dòng raw
    return json.loads(line.decode())

while True:
    print("\n[+] Opening connection...")
    r = remote(HOST, PORT)

    # 1) encrypt_data với 32 byte 0x00
    print("[+] Sending encrypt_data...")
    r.recvuntil(b"Gotta go fast!\n")
    payload = {"option": "encrypt_data", "input_data": "00" * 32}
    r.sendline(json.dumps(payload).encode())
    resp = recv_json_line(r)
    enc_zeros_hex = resp["encrypted_data"]
    enc_zeros = bytes.fromhex(enc_zeros_hex)
    print("[DEBUG] enc_zeros_hex =", enc_zeros_hex)

    # 2) get_flag
    print("[+] Sending get_flag...")
    r.sendline(json.dumps({"option": "get_flag"}).encode())
    resp = recv_json_line(r)
    enc_flag_hex = resp["encrypted_flag"]
    enc_flag = bytes.fromhex(enc_flag_hex)
    print("[DEBUG] enc_flag_hex =", enc_flag_hex)

    r.close()

    # 3) XOR giải mã
    keystream = enc_zeros[:len(enc_flag)]
    flag_bytes = strxor(enc_flag, keystream)
    print("[DEBUG] flag candidate bytes =", flag_bytes)

    try:
        flag_str = flag_bytes.decode()
        print("[DEBUG] flag candidate str =", flag_str)
    except UnicodeDecodeError:
        print("[DEBUG] decode fail, raw bytes shown above")
        flag_str = ""

    # 4) kiểm tra prefix crypto{
    if flag_str.startswith("crypto{") and flag_str.endswith("}"):
        print("\n[+] GOT FLAG:", flag_str)
        break
    else:
        print("[!] Wrong candidate, retrying...\n")
