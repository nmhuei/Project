#!/usr/bin/env python3
# exploit_prosign3.py
import json
import hashlib
from random import randrange
from pwn import remote
from Crypto.Util.number import bytes_to_long, inverse
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192

# remote server settings (the challenge uses these)
HOST = "socket.cryptohack.org"
PORT = 13381

g = generator_192
N = g.order()

def sha1_long(m: bytes) -> int:
    return bytes_to_long(hashlib.sha1(m).digest())

def ask_sign_time(rconn):
    rconn.sendline(json.dumps({"option": "sign_time"}).encode())
    line = rconn.recvline(timeout=5)
    return json.loads(line.decode())

def ask_verify(rconn, msg, r_hex, s_hex):
    payload = {"option": "verify", "msg": msg, "r": r_hex, "s": s_hex}
    rconn.sendline(json.dumps(payload).encode())
    line = rconn.recvline(timeout=5)
    return json.loads(line.decode())

def try_recover_and_unlock(rconn):
    print("[*] Requesting a time-signature from server...")
    signed = ask_sign_time(rconn)
    print("[*] Received:", signed)

    msg = signed["msg"]
    r_int = int(signed["r"], 16)
    s_int = int(signed["s"], 16)
    e = sha1_long(msg.encode())

    print(f"[*] msg = {msg!r}")
    print(f"[*] r = {r_int} (0x{r_int:x}), s = {s_int} (0x{s_int:x})")
    print("[*] Hash e =", e)

    # k on server is chosen with randrange(1, n_local) where n_local = seconds (0..59) -> small
    # brute-force k in 1..59 (skip k that make r==0 or invalid)
    for k_guess in range(1, 60):
        try:
            # d = (s*k - e) * r^{-1} mod N
            inv_r = inverse(r_int, N)
            d_cand = ( (s_int * k_guess - e) * inv_r ) % N

            # sanity: d must be in [1, N-1]
            if d_cand <= 0 or d_cand >= N:
                continue

            # build keys from candidate d
            pub_cand = Public_key(g, g * d_cand)
            priv_cand = Private_key(pub_cand, d_cand)

            # sign "unlock" using this candidate private key
            target_msg = "unlock"
            e_unlock = sha1_long(target_msg.encode())
            k2 = randrange(1, N)
            sig2 = priv_cand.sign(e_unlock, k2)

            r_hex = hex(sig2.r)
            s_hex = hex(sig2.s)

            print(f"[*] Trying k={k_guess}, d_candidate=0x{d_cand:x}")
            resp = ask_verify(rconn, target_msg, r_hex, s_hex)
            print("[*] verify response:", resp)
            if "flag" in resp:
                print("\n[+] GOT FLAG:\n", resp["flag"])
                return True
            # sometimes server may respond with "Message verified" even if not unlock; keep trying
        except Exception as exc:
            # ignore invalid math (e.g., inverse failure)
            # print(f"[!] k={k_guess} raised {exc}")
            continue

    print("[-] Tried all k in 1..59 but did not get flag.")
    return False

def main():
    print("[*] Connecting to remote...")
    rconn = remote(HOST, PORT, timeout=10)
    rconn.recvline()
    try:
        success = try_recover_and_unlock(rconn)
        if not success:
            print("[-] Exploit failed. You can try requesting a fresh signature and re-run.")
    finally:
        rconn.close()

if __name__ == "__main__":
    main()
