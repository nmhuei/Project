from pwn import *
import json
from Crypto.Util.number import *

context.log_level = "DEBUG"

HOST, PORT = "socket.cryptohack.org", 13399
r = remote(HOST, PORT)

def send_cmd(r, payload):
    r.sendline(json.dumps(payload).encode())
    return r.recvline().decode()

def repeat_hex_to_int(i, repeat=4):
    # chuyển sang hex 2 ký tự (padding bằng 0 nếu cần)
    h = format(i, "02x")
    # lặp lại
    s = h * repeat
    # đổi sang int
    return int(s, 16)

while True:
    send_cmd(r, {"option": "reset_connection"})
    send_cmd(r, {"option": "reset_password", "token": long_to_bytes(0, 128).hex()})
    res = send_cmd(r, {"option": "authenticate", "password": ""})
    
    if "flag" in res:
        print(res)
        exit()
        
        
    
    