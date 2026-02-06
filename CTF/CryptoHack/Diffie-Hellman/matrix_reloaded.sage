#!/usr/bin/env sage
# -*- coding: utf-8 -*-

import json
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
from sage.all import GF, Matrix, vector, crt, identity_matrix

# ===== Tham số =====
P = 13322168333598193507807385110954579994440518298037390249219367653433362879385570348589112466639563190026187881314341273227495066439490025867330585397455471
N = 30
KEY_LENGTH = 128  # digest()[:KEY_LENGTH] -> thực tế 32 bytes => AES-256

# ===== Đọc dữ liệu =====
def load_matrix(fname):
    rows = [list(map(int, row.split())) for row in open(fname).read().strip().splitlines()]
    return Matrix(GF(P), rows)

F = GF(P)
G = load_matrix("generator.txt")

with open("output.txt", "r") as f:
    data = json.load(f)
vF = vector(F, data["v"])
wF = vector(F, data["w"])

with open("flag.enc", "r") as f:
    enc = json.load(f)
iv = unhexlify(enc["iv"])
ct = unhexlify(enc["ciphertext"])

# u = G * v
uF = G * vF


print(len(vF))