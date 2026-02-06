import secrets
import string

def generate_strong_password(length=24):
    if length < 4:
        raise ValueError("Password length must be at least 4")

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}<>?"

    # Bắt buộc mỗi loại ít nhất 1 ký tự
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    # Các ký tự còn lại
    all_chars = lowercase + uppercase + digits + symbols
    password += [secrets.choice(all_chars) for _ in range(length - 4)]

    # Trộn ngẫu nhiên để tránh lộ cấu trúc
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

if __name__ == "__main__":
    print("Generated password:", generate_strong_password(24))
