#!/usr/bin/env python3
# exploit.py
# Requires: pwntools (pip install pwntools)
# Usage: python3 exploit.py [host] [port]
#
# This script:
#  - connects to the challenge service
#  - extracts master_key_enc, share_key_enc, share_key_pub (if present in banner)
#  - does wait_login to create the login object on server
#  - replays the two ciphertext blobs into send_challenge to get the RSA-decryption oracle
#  - provides oracle(ct_bytes) -> plaintext bytes
#
# Next step: implement prime recovery using Bleichenbacher / GaP and the oracle.
# I can implement the full prime recovery if you want — say "continue" and I'll write it.

from pwn import *
from Crypto.Util.number import*
import sys
import json
import binascii
import re

context.log_level = 'info'

HOST, PORT = "socket.cryptohack.org", 13408

# If banner parse fails, you may paste the hexes here as fallback:
FALLBACK_master_key_enc_hex = None
FALLBACK_share_key_enc_hex = None
FALLBACK_share_key_pub = None  # e.g. [n, e] tuple or None


def try_extract_json_from_banner(s):
    """
    Try to find the JSON 'material' printed in the banner:
    It looks like:
      ... New client is uploading crypto material...
      {"auth_key_hashed": "...", "master_key_enc": "....", "share_key_pub": [n,e], "share_key_enc": "..."}
    Return parsed dict or None.
    """
    # naive extraction of JSON blob between first '{' that contains "master_key_enc" and its matching '}'
    try:
        start = s.index(b'{')
        # find the substring that contains masters
        subs = s[start:].decode(errors='ignore')
        # find the JSON object by regex that contains master_key_enc
        m = re.search(r'(\{.*?"master_key_enc"\s*:\s*".*?".*?\})', subs, flags=re.S)
        if m:
            j = m.group(1)
            return json.loads(j)
    except Exception:
        pass
    return None


def connect_and_get_banner():
    io = remote(HOST, PORT, timeout=5)
    # read some initial data
    try:
        banner = io.recvrepeat(timeout=0.8)
    except Exception:
        banner = b''
    return io, banner


def start_session_and_create_oracle(io, master_key_enc_hex, share_key_enc_hex):
    """
    Performs wait_login, then uses send_challenge with provided ciphertext blobs to create oracle.
    Returns a function oracle(ct_bytes) -> plaintext_bytes.
    """
    # 1) send wait_login
    pkt = {"action": "wait_login"}
    io.sendline(json.dumps(pkt).encode())
    # read one line response
    resp_line = io.recvline(timeout=2).decode(errors='ignore').strip()
    try:
        resp = json.loads(resp_line)
    except Exception:
        # maybe multiple lines: try to read more
        remaining = io.recvrepeat(timeout=0.2)
        try:
            resp = json.loads((resp_line + remaining.decode()).strip())
        except Exception:
            resp = {}
    log.info(f"wait_login response: {resp}")

    # build oracle
    def oracle(ct_bytes):
        """
        ct_bytes: raw ciphertext bytes (RSA ciphertext)
        returns plaintext bytes (server returns hex of SID then we convert to bytes)
        """
        SID_enc_hex = ct_bytes.hex()
        payload = {
            "action": "send_challenge",
            "SID_enc": SID_enc_hex,
            "share_key_enc": share_key_enc_hex,
            "master_key_enc": master_key_enc_hex
        }
        io.sendline(json.dumps(payload).encode())
        # read a response line
        line = io.recvline(timeout=4)
        if not line:
            # try to read more and return None
            more = io.recvrepeat(timeout=0.5)
            line = more
        try:
            j = json.loads(line.decode())
        except Exception:
            # sometimes there might be an extra prompt; try to parse any JSON in the response
            txt = line.decode(errors='ignore')
            m = re.search(r'(\{.*\})', txt, flags=re.S)
            if m:
                try:
                    j = json.loads(m.group(1))
                except Exception:
                    return None
            else:
                return None
        if "error" in j:
            log.info(f"oracle call error: {j['error']}")
            return None
        if "SID" in j:
            # server returns SID hex string of plaintext (they returned SID = long_to_bytes(m).hex())
            try:
                return bytes.fromhex(j["SID"])
            except Exception:
                return None
        else:
            return None

    return oracle


def get_encrypted_flag(io):
    io.sendline(json.dumps({"action": "get_encrypted_flag"}).encode())
    line = io.recvline(timeout=2).decode(errors='ignore').strip()
    try:
        j = json.loads(line)
    except Exception:
        # try to extract json from partial output
        more = io.recvrepeat(timeout=0.2)
        try:
            j = json.loads((line + more.decode()).strip())
        except Exception:
            return None
    if "encrypted_flag" in j:
        return bytes.fromhex(j["encrypted_flag"])
    return None


def main():
    io, banner = connect_and_get_banner()
    log.info("Banner / pre-input:")
    log.info(banner.decode(errors='ignore'))

    parsed = try_extract_json_from_banner(banner)
    master_hex = None
    share_hex = None
    share_pub = None
    if parsed:
        log.info(f"Found JSON material in banner: {parsed.keys()}")
        master_hex = parsed.get("master_key_enc")
        share_hex = parsed.get("share_key_enc")
        share_pub = parsed.get("share_key_pub")
    else:
        log.warning("Could not auto-parse JSON in banner.")
        # fallback: use manually filled values if provided
        if FALLBACK_master_key_enc_hex and FALLBACK_share_key_enc_hex:
            master_hex = FALLBACK_master_key_enc_hex
            share_hex = FALLBACK_share_key_enc_hex
            share_pub = FALLBACK_share_key_pub
        else:
            # prompt user to paste them
            print("Please paste master_key_enc hex (or set FALLBACK_* values in script):")
            master_hex = input().strip()
            print("Please paste share_key_enc hex:")
            share_hex = input().strip()
            try:
                print("Paste share_key_pub as JSON [n,e] or press Enter to skip:")
                t = input().strip()
                if t:
                    share_pub = json.loads(t)
            except Exception:
                share_pub = None

    if not master_hex or not share_hex:
        log.error("Missing ciphertext blobs; abort.")
        return

    log.info("Using master_key_enc (hex) length=%d" % len(master_hex))
    log.info("Using share_key_enc (hex) length=%d" % len(share_hex))
    if share_pub:
        try:
            n = int(share_pub[0])
            e = int(share_pub[1])
            log.info(f"Found share_key_pub: n bitlen={n.bit_length()} e={e}")
        except Exception:
            n = None
            e = None
    else:
        n = None
        e = None

    # create oracle
    oracle = start_session_and_create_oracle(io, master_hex, share_hex)
    # quick test: ask oracle to decrypt small ciphertexts
    # Here we craft a small ciphertext: 1^e mod n (i.e., 1) => decrypt => 1 (bytes)
    if n and e:
        c_one = pow(1, e, n)
        c_bytes = long_to_bytes(c_one) if 'long_to_bytes' in globals() else (c_one.to_bytes((c_one.bit_length()+7)//8 or 1, 'big'))
        # pad to typical RSA ciphertext length in hex? Not necessary; server treats SID_enc as bytes->long
        out = oracle(c_bytes)
        log.info(f"Oracle(1) -> {out}")
    else:
        # ask user for a sample ciphertext to test, or try a small default
        test_c = bytes([0x02])
        out = oracle(test_c)
        log.info(f"Oracle(0x02) -> {out}")

    # get encrypted flag (AES-ECB)
    enc_flag = get_encrypted_flag(io)
    if enc_flag:
        log.info(f"Encrypted flag (hex): {enc_flag.hex()}")
        # We cannot decrypt it until we recover p,q -> secret = SHA256(p||q)
    else:
        log.warning("Could not fetch encrypted flag (maybe service logged out?)")

    log.info("Now you have an RSA-decryption oracle as `oracle(ct_bytes)`.")
    log.info("Next: implement factor-recovery using the oracle (Bleichenbacher / GaP).")
    log.info("I can implement the prime-recovery code next if you want — say 'continue' and I'll write the code to recover p and q using the oracle.")
    # keep socket open for interactive testing
    io.interactive()


if __name__ == "__main__":
    main()
