import sympy as sp
import hashlib
import sys

ITERS = int(2e7)
VERIF_KEY = "96cc5f3b460732b442814fd33cf8537c"
ENCRYPTED_FLAG = bytes.fromhex("42cbbce1487b443de1acf4834baed794f4bbd0dfe7d7086e788af7922b")

# Ma trận chuyển trạng thái
A = sp.Matrix([
    [21, 301, -9549, 55692],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]
])

# Vector khởi tạo [m(3), m(2), m(1), m(0)]
init = sp.Matrix([4, 3, 2, 1])

def solve_m(n: int):
    if n == 0: return 1
    if n == 1: return 2
    if n == 2: return 3
    if n == 3: return 4

    # Tính A^(n-3) * init
    M = A**(n-3)   # sympy dùng số nguyên arbitrary precision
    res = M * init
    return int(res[0])

def decrypt_flag(sol: int):
    import sys
    sys.set_int_max_str_digits(1000000)  # tăng giới hạn
    sol = sol % (10**10000)       # lấy 10000 chữ số cuối
    sol = str(sol)
    sol_md5 = hashlib.md5(sol.encode()).hexdigest()

    if sol_md5 != VERIF_KEY:
        print("❌ Incorrect solution")
        sys.exit(1)

    key = hashlib.sha256(sol.encode()).digest()
    flag = bytearray([char ^ key[i] for i, char in enumerate(ENCRYPTED_FLAG)]).decode()
    print("✅ Flag:", flag)

if __name__ == "__main__":
    print("⏳ Đang tính m(%d)..." % ITERS)
    sol = solve_m(ITERS)
    decrypt_flag(sol)
