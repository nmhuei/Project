from sage.all import *

E = 31337

# 1) đọc file ciphertext
with open("flag.enc", "r") as f:
    data = f.read().strip().splitlines()

rows = [[int(b) for b in row] for row in data]
C = Matrix(GF(2), rows)

# 2) tính order của C
ordC = C.multiplicative_order()
print("[+] ord(C) =", ordC)

# 3) kiểm tra gcd
if gcd(E, ordC) != 1:
    print("[-] gcd(E, ord(C)) != 1 → không thể đảo trực tiếp, cần discrete log.")
else:
    # 4) tính nghịch đảo modular
    d = inverse_mod(E, ordC)
    print("[+] d =", d)

    # 5) giải mã: M = C^d
    M = C^d

    # 6) trích bits theo column-major (giống khi generate_mat)
    bits = []
    for col in range(M.ncols()):
        for row in range(M.nrows()):
            bits.append(int(M[row, col]))

    # gộp thành bytes
    bitstring = "".join(str(b) for b in bits)
    bs = bytes(int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8))

    # 7) tìm flag trong bytes
    start = bs.find(b"crypto{")
    end   = bs.find(b"}", start)
    if start != -1 and end != -1:
        flag = bs[start:end+1]
        print("[+] FLAG =", flag.decode())
    else:
        print("[-] Không tìm thấy flag, có thể đọc sai thứ tự bits.")
