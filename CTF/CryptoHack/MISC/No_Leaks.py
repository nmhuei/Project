from pwn import remote, context
import json, base64, time

context.log_level = "debug"

HOST, PORT = "socket.cryptohack.org", 13370
N = 20

# Các ký tự flag đã biết
KNOWN = {
    0: ord('c'),
    1: ord('r'),
    2: ord('y'),
    3: ord('p'),
    4: ord('t'),
    5: ord('o'),
    6: ord('{'),
    19: ord('}'),
}

def fetch_ciphertext_once(idx):
    try:
        r = remote(HOST, PORT, timeout=5.0)
    except Exception:
        return None
    try:
        try:
            r.recvuntil(b"No leaks\n")
        except Exception:
            pass
        r.sendline(json.dumps({"msg":"request"}).encode())
        line = r.recvline().strip()
        resp = json.loads(line.decode())
        if "ciphertext" not in resp:
            return None
        return base64.b64decode(resp["ciphertext"])
    except Exception:
        return None
    finally:
        try:
            r.close()
        except Exception:
            pass

def recover_flag():
    seen = [set() for _ in range(N)]
    flag = bytearray(b'?'*N)

    # điền sẵn các ký tự đã biết
    for i, v in KNOWN.items():
        flag[i] = v

    conn_idx = 0
    t0 = time.time()

    while True:
        conn_idx += 1
        ct = fetch_ciphertext_once(conn_idx)
        if ct is None:
            continue

        for i, b in enumerate(ct[:N]):
            if i in KNOWN:
                continue   # bỏ qua vị trí đã biết
            seen[i].add(b)

        # kiểm tra vị trí nào đã đủ 255 giá trị
        for i in range(N):
            if i in KNOWN:
                continue
            if flag[i] == ord('?') and len(seen[i]) >= 255:
                missing = set(range(256)) - seen[i]
                if len(missing) == 1:
                    flag[i] = missing.pop()
                    print(f"[+] Found position {i}: {chr(flag[i])}")

        # nếu xong hết
        if all(flag[i] != ord('?') for i in range(N)):
            break

        if conn_idx % 100 == 0:
            elapsed = time.time() - t0
            print(f"[prog] conn={conn_idx} elapsed={elapsed:.1f}s")

    return flag, conn_idx, time.time()-t0

if __name__ == "__main__":
    flag, total, elapsed = recover_flag()
    print(f"[done] connections={total}, time={elapsed:.1f}s")
    print("[+] FLAG:", flag.decode())

# vl 
# [done] connections=2726, time=2092.3s
# [+] FLAG: crypto{unr4nd0m_07p}