# save as find_btc.py
import hashlib
from ecdsa import SigningKey, SECP256k1
import base58
from multiprocessing import Pool, cpu_count, Manager
import secrets
import sys

# hàm kiểm tra Base58Check tương đương btc_check
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def btc_check(addr):
    try:
        raw = base58.b58decode(addr)
    except Exception:
        return False
    if len(raw) < 5:
        return False
    version = raw[0]
    if version not in (0, 5):
        return False
    checksum = raw[-4:]
    payload = raw[:-4]
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return chk == checksum

def pubkey_compressed_from_sk(sk: SigningKey) -> bytes:
    vk = sk.get_verifying_key()
    xb = vk.to_string()[:32]
    yb = vk.to_string()[32:]
    prefix = b'\x02' if (yb[-1] % 2 == 0) else b'\x03'
    return prefix + xb

def key_to_p2pkh(pub: bytes) -> str:
    vh160 = b'\x00' + hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    checksum = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()[:4]
    return base58.b58encode(vh160 + checksum).decode()

# worker: sinh address, trả (priv_hex, addr) khi addr thỏa predicate
def worker(args):
    prefix, target_count, outq = args
    # outq is Manager().list or Queue for early stop support
    while True:
        sk = SigningKey.generate(curve=SECP256k1)
        pub = pubkey_compressed_from_sk(sk)
        addr = key_to_p2pkh(pub)
        if prefix:
            ok = addr.startswith(prefix)
        else:
            ok = True  # trả mọi địa chỉ hợp lệ
        if ok:
            priv_hex = sk.to_string().hex()
            outq.append((priv_hex, addr))
            # if we reached enough results, return to let main stop pool
            if len(outq) >= target_count:
                return

def find_addresses(prefix="", count=1, processes=None):
    if processes is None:
        processes = max(1, cpu_count()-0)  # you can leave one core
    mgr = Manager()
    outq = mgr.list()
    args = [(prefix, count, outq) for _ in range(processes)]
    with Pool(processes) as p:
        p.map(worker, args)   # will return when workers finish
        p.terminate()
    return list(outq)[:count]

if __name__ == "__main__":
    # usage: python find_btc.py [prefix] [count]
    pref = sys.argv[1] if len(sys.argv) > 1 else ""
    cnt = int(sys.argv[2]) if len(sys.argv) > 2 else 2

    print(f"Searching for {cnt} addresses with prefix '{pref}' using {cpu_count()} cores...")
    res = find_addresses(prefix=pref, count=cnt)
    for i, (priv, addr) in enumerate(res):
        print(f"[{i}] addr = {addr}  priv_hex = {priv}  btc_check = {btc_check(addr)}")
