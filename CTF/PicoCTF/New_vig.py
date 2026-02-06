import string

# constants
LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]  # a–p (16 ký tự)

# -----------------------------
# Giải mã B16 (base16 alphabet)
# -----------------------------
def b16_decode(cipher):
    dec = ""
    for c in range(0, len(cipher), 2):
        b = ""
        b += "{0:b}".format(ALPHABET.index(cipher[c])).zfill(4)
        b += "{0:b}".format(ALPHABET.index(cipher[c + 1])).zfill(4)
        dec += chr(int(b, 2))
    return dec

# -----------------------------
# Dịch ngược (reverse Caesar)
# -----------------------------
def unshift(c, k):
    t1 = ord(c) - LOWERCASE_OFFSET
    t2 = ord(k) - LOWERCASE_OFFSET
    return ALPHABET[(t1 - t2) % len(ALPHABET)]

# -----------------------------
# Thử các khóa khả dĩ (đệ quy)
# -----------------------------
def get_key(s, matrix):
    # Nếu chỉ còn 1 danh sách con (tức là đang ở vị trí cuối cùng)
    if len(matrix) == 1:
        for a in ALPHABET:
            k = str(s) + str(a)
            pt = ""
            for i, c in enumerate(enc):
                pt += unshift(c, k[i % len(k)])
            pt = b16_decode(pt)
            if all(c in "abcdef0123456789" for c in pt):
                print(f"Possible plaintext: {pt}")
                print(f"Key: {k}")
        return

    # Nếu chưa đến cuối, đệ quy tiếp
    for x in matrix[0]:
        s2 = str(s) + str(x)
        get_key(s2, matrix[1:len(matrix)])

# -----------------------------
# Dữ liệu mã hóa
# -----------------------------
enc = "bkglibgkhghkijphhhejggikgjkbhefgpienefjdioghhchffhmmhhbjgclpjfkp"

# Mảng chứa các key hợp lệ ở từng vị trí
keys = [[] for _ in range(32)]

# -----------------------------
# Tạo tất cả các cặp key (2 ký tự)
# -----------------------------
for a in ALPHABET:
    for b in ALPHABET:
        key = str(a) + str(b)
        pt = ""

        for i, c in enumerate(enc):
            pt += unshift(c, key[i % len(key)])

        pt = b16_decode(pt)

        for cur in range(len(pt)):
            if pt[cur] in "abcdef0123456789":
                keys[cur].append(key)

# In ra danh sách key khả dĩ
for idx, key_list in enumerate(keys):
    print(f"[{idx}] {key_list}")

# -----------------------------
# Giải thử 5 ký tự đầu (giới hạn để tránh quá tải)
# -----------------------------
get_key("", keys[0:5])
