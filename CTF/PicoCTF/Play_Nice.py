from pwn import remote
from Crypto.Util.number import bytes_to_long, long_to_bytes

SQUARE_SIZE = 6

def generate_square(alphabet):
    assert len(alphabet) == pow(SQUARE_SIZE, 2)
    matrix = []
    for i, letter in enumerate(alphabet):
        if i % SQUARE_SIZE == 0:
            row = []
        row.append(letter)
        if i % SQUARE_SIZE == (SQUARE_SIZE - 1):
            matrix.append(row)
    return matrix

def get_index(letter, matrix):
    for row in range(SQUARE_SIZE):
        for col in range(SQUARE_SIZE):
            if matrix[row][col] == letter:
                return (row, col)
    raise ValueError("letter not found")

def decrypt_pair(pair, matrix):
    p1 = get_index(pair[0], matrix)
    p2 = get_index(pair[1], matrix)

    if p1[0] == p2[0]:  # cùng hàng
        return matrix[p1[0]][(p1[1] - 1) % SQUARE_SIZE] + matrix[p2[0]][(p2[1] - 1) % SQUARE_SIZE]
    elif p1[1] == p2[1]:  # cùng cột
        return matrix[(p1[0] - 1) % SQUARE_SIZE][p1[1]] + matrix[(p2[0] - 1) % SQUARE_SIZE][p2[1]]
    else:  # hình chữ nhật
        return matrix[p1[0]][p2[1]] + matrix[p2[0]][p1[1]]

def decrypt_string(s, matrix):
    result = ""
    for i in range(0, len(s), 2):
        result += decrypt_pair(s[i:i+2], matrix)
    return result

def main():
    HOST, PORT = "mercury.picoctf.net", 30568
    r = remote(HOST, PORT)

    # đọc tới phần alphabet + encrypted message:
    data = r.recvuntil(b"encrypted message:").decode()
    alphabet_line = data.split("alphabet: ")[1].split("\n")[0].strip()

    # dòng tiếp theo là ciphertext
    enc_msg = r.recvline().decode().strip()

    print("[+] Alphabet:", alphabet_line)
    print("[+] Encrypted:", enc_msg)

    # tạo ma trận
    m = generate_square(alphabet_line)

    # giải mã
    plain = decrypt_string(enc_msg, m)
    print("[+] Plaintext guess:", plain)

    # gửi lại
    r.sendline(plain.encode())

    # in kết quả
    print(r.recvall().decode())


if __name__ == "__main__":
    main()
