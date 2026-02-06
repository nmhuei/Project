# attack_runner.py
from pwn import *
from tqdm import tqdm
import json
import time
import traceback

context.log_level = 'info'

HOST = "socket.cryptohack.org"
PORT = 13423
BLOCK_SIZE = 16

# ---------- attack logic (unchanged, but uses a given connected 'r') ----------
def get_ct(r):
    r.sendline(json.dumps({"option": "encrypt"}).encode())
    res = json.loads(r.recvline().decode())["ct"]
    return res

def oracle(r, ct, k = 20):
    true = 0
    false = 0
    for _ in range(k):
        r.sendline(json.dumps({"option": "unpad", "ct": ct.hex()}).encode())
        res = json.loads(r.recvline().decode())["result"]
        if res == False:
            false += 1
        else:
            true += 1
    return 1 if false > true else 0

def count_iv_block(iv, pad_val):
    charset = b'1234567890abcdef'
    x = iv[-pad_val]
    return sorted(set([x ^ c ^ pad_val for c in charset]))

def solve_pt_block(r, block, iv_bytes):
    zeroing_iv = [0] * BLOCK_SIZE
    for pad_val in tqdm(range(1, BLOCK_SIZE + 1)):
        padding_iv = [pad_val ^ b for b in zeroing_iv]
        iv_block = count_iv_block(iv_bytes, pad_val)

        for c in iv_block:
            padding_iv[-pad_val] = c
            iv = bytes(padding_iv)
            if oracle(r, iv + block):
                if pad_val == 1:
                    padding_iv[-2] ^= 1
                    iv2 = bytes(padding_iv)
                    if not oracle(r, iv2 + block):
                        continue
                break
        else:
            raise Exception(f'[*] Invalid value for pad {pad_val}! candidates exhausted')

        zeroing_iv[-pad_val] = c ^ pad_val
        # debug prints (optional)
        # print("padding_iv:", padding_iv)
        # print("zeroing_iv :", zeroing_iv)

    return zeroing_iv

def AES_CBC_Attack_Full(r, msg_hex):
    msg = bytes.fromhex(msg_hex)
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    if len(blocks) < 2:
        raise ValueError("Ciphertext must contain IV + at least one block")

    iv = blocks[0]
    result = b''

    for block in blocks[1:]:
        dec = solve_pt_block(r, block, iv)
        pt = bytes([iv_bytes ^ dec_bytes for iv_bytes, dec_bytes in zip(iv, dec)])
        result += pt
        iv = block
        print('[*] Partial result:', result)
    return result

# ---------- runner/wrapper ----------
def run_attack(max_retries=100, backoff=3, initial_wait=1):
    attempts = 0
    while attempts < max_retries:
        attempts += 1
        r = None
        try:
            print(f"[+] Attempt {attempts}/{max_retries} — connecting to {HOST}:{PORT}")
            r = remote(HOST, PORT)
            # read initial greeting line(s) if present
            try:
                r.recvline(timeout=1)
            except Exception:
                pass

            # fetch ct
            ct_hex = get_ct(r)
            print("[+] Received ciphertext (hex len):", len(ct_hex))
            # run attack
            plaintext = AES_CBC_Attack_Full(r, ct_hex)
            try:
                pw = plaintext.decode()
            except Exception:
                pw = plaintext.decode(errors='ignore')
            print("[+] Final plaintext (raw):", plaintext)
            # check length expected before send
            if len(pw) != 32:
                print(f"[!] Warning: pw length is {len(pw)} (expected 32). Still sending to check.")
            # send check
            r.sendline(json.dumps({"option": "check", "message": pw}).encode())
            print(r.recvall(timeout=5))
            # success — close and return
            r.close()
            return True
        except KeyboardInterrupt:
            print("[!] Interrupted by user. Exiting.")
            if r:
                try: r.close()
                except: pass
            return False
        except Exception as e:
            print(f"[!] Attempt {attempts} failed with exception:")
            traceback.print_exc()
            if r:
                try:
                    r.close()
                except Exception:
                    pass
            if attempts < max_retries:
                wait = backoff * attempts
                print(f"[+] Sleeping {wait}s before retrying...")
                time.sleep(wait)
            else:
                print("[!] Reached max_retries. Giving up.")
                return False

if __name__ == "__main__":
    # small initial delay to let you attach debugger/log if needed
    time.sleep(1)
    success = run_attack(max_retries=6, backoff=2)
    if success:
        print("[+] Attack finished successfully.")
    else:
        print("[!] Attack did not succeed.")
