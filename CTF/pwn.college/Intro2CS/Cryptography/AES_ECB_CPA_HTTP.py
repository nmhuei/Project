#!/usr/bin/env python3
# sql_brute_simple.py — chạy thẳng, không cần args
import requests, string, time, re, sys

URL = "http://challenge.localhost/"   # chỉnh nếu cần
PREFIX = "pwn.college{"
MAXLEN = 60
TIMEOUT = 5.0
DELAY = 0.01

RE_CT = re.compile(r"<b>Results:</b>\s*<pre>\s*([0-9a-fA-F]+)\s*</pre>", re.I|re.S)

def get_ct(q):
    r = requests.get(URL, params={"query": q}, timeout=TIMEOUT)
    r.raise_for_status()
    m = RE_CT.search(r.text)
    if not m:
        raise RuntimeError("No ciphertext in response")
    return m.group(1).strip()

def literal(s):
    return "'" + s.replace("'", "''") + "'"

# build charset (printable without newline, prioritized)
_printable = string.printable.replace("\n","").replace("\r","")
PRIORITY = '_}' + string.digits + string.ascii_lowercase + string.ascii_uppercase
OTHER = ''.join(ch for ch in _printable if ch not in PRIORITY)
CHARSET = list((PRIORITY + OTHER))

def brute():
    flag = PREFIX
    while not flag.endswith('}'):
        n = len(flag) + 1
        try:
            target = get_ct(f"substr(flag,1,{n})")
        except Exception as e:
            print("[!] Error fetching target substr:", e); return None
        found = None
        print(f"[+] {flag}", end="", flush=True)
        for ch in CHARSET:
            cand = flag + ch
            try:
                ct = get_ct(literal(cand))
            except Exception as e:
                print("\n[!] HTTP error:", e); return None
            if ct == target:
                found = ch
                break
            time.sleep(DELAY)
        if not found:
            print("\n[!] Next char not found. Consider increasing MAXLEN or expanding CHARSET.")
            return None
        flag += found
        print(f" -> {found}")
        if len(flag) > MAXLEN:
            print("[!] Reached MAXLEN"); return None
    return flag

if __name__ == "__main__":
    print("[*] URL:", URL, "PREFIX:", PREFIX, "MAXLEN:", MAXLEN)
    res = brute()
    if res:
        print("[*] FLAG:", res)
    else:
        print("[!] Failed.")
