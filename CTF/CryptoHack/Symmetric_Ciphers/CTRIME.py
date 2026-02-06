import requests, string

URL = "https://aes.cryptohack.org/ctrime/encrypt/"

def encrypt(pt: str) -> int:
    r = requests.get(f"{URL}{pt.encode().hex()}/")
    ct = r.json()["ciphertext"]
    return len(ct)//2   # số byte

charset = "}_" + string.digits + string.ascii_uppercase + string.ascii_lowercase
flag = "crypto{CRIME_571ll_p4y5}"
flag = "crypto{"
while not flag.endswith("}"):
    best_len = 10**9
    best_ch = None
    check = [0] * 1000
    for ch in charset:
        test = flag + ch
        length = encrypt(test)
        print(f"[*] Try with {ch}: {length}")
        if length < best_len:
            best_len = length
            best_ch = ch
            
    flag += best_ch
    print("[+] flag so far:", flag)
