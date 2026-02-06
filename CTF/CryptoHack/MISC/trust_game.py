from pwn import *
from Crypto.Util.number import *
from Crypto.Cipher import AES
import json

context.log_level = "warning"
HOST, PORT = "socket.cryptohack.org", 13396

a = 0x1337deadbeef
b = 0xb
m = 2**48

soc = remote(HOST, PORT)

class LCG:
    def __init__(self, a, b, m, seed):
        self.a = a
        self.b = b
        self.m = m
        self.state = seed
        self.counter = 0

    def refresh(self):
        self.counter = 0
        self.state = bytes_to_long(urandom(6))

    def next_state(self):
        self.state = (self.a * self.state + self.b) % self.m

    def get_random_bits(self, k):
        if self.counter == 16:
            self.refresh()
        self.counter += 1
        self.next_state()
        return self.state >> (48 - k)

    def get_random_bytes(self, number):
        bytes_sequence = b''
        for i in range(number):
            bytes_sequence += bytes([self.get_random_bits(8)])
        return bytes_sequence
        
def get_a_challenge(soc):
    payload = {
        "option" : "get_a_challenge"
    }
    
    soc.sendline(json.dumps(payload).encode())
    res = json.loads(soc.recvline().decode())
    try:
        return res["plaintext"], res["IV"]
    except:
        print("[*] Somethings wrong in get_a_challenge function!!!")

def validate(soc, ciphertext = b"Hello, World"):
    ciphertext = hex(bytes_to_long(ciphertext))[2:]
    payload = {
        "option" : "validate",
        "ciphertext" : ciphertext 
    }
    
    soc.sendline(json.dumps(payload).encode())
    res = json.loads(soc.recvline().decode())
    msg = res["msg"]
    
    if "flag" in msg:
        return f"[*] Congratuation!!! Here's your flag {msg.split()[-1]}"
    else:
        return msg

def decrypt(key : bytes, plaintext : bytes, IV : bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, IV)
    my_ct = cipher.encrypt(plaintext)
    
    return my_ct

def find_seed(P1 : str, P2 : str):
    P1 = int(P1, 16)
    P2 = int(P2, 16)
    
    print(P1, P2)
    
    L1 = P1 * (2 ** 40)
    L2 = (P2 * (2 ** 40) - b) // a 
    H1 = (P1 + 1) * (2 ** 40) - 1
    H2 = ((P2 + 1) * (2 ** 40)) // a
    
    print(L1, L2, H1, H2)
    
    
    x = max(L1, L2)
    y = min(H1, H2)
    
    print(x)
    print(y)
    
def recover_seed(tops, a = a, b = b, m = m):
    # tops = danh sách top8[state_i] quan sát từ server
    
    candidates = []

    # Khởi tạo 256 khả năng ứng với 8 bit thấp đầu tiên
    for low8 in range(256):
        s0 = (tops[0] << 40) | low8
        s1 = (a*s0 + b) % m
        if (s1 >> 40) == tops[1]:
            candidates.append(s0)

    # Mỗi vòng thêm 8 bit (5 vòng để có 40 bit)
    for round in range(1, 5):
        new_cands = []
        for cand in candidates:
            for add8 in range(256):
                s0 = cand | (add8 << (8*round))
                s1 = (a*s0 + b) % m
                if (s1 >> 40) == tops[1]:
                    new_cands.append(s0)
        candidates = new_cands

    # Kiểm tra khớp cả chuỗi
    for s0 in candidates:
        ok = True
        s = s0
        for t in tops:
            if (s >> 40) != t:
                ok = False
                break
            s = (a*s + b) % m
        if ok:
            return s0  # đây là seed thật
    return None
    
id_player = soc.recvline().decode().split(".")[0].split()[-1]

print(f"[*] ID Player : {id_player}")
try:
    plaintext, IV = get_a_challenge(soc)
    print(f"[*] Plaintext : {plaintext}")
    print(f"[*] IV : {IV}")
    
    seed = recover_seed(id_player)
    print(seed)
    G = LCG(seed)
    data = G.get_random_bytes(16)[8:]
    data_hex = hex(int(data))[2:] 
    print(data_hex)
    
    print(validate(soc))

except:
    print()

