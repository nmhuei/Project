import requests

def encrypt(pt):
    plain_hex = pt.encode().hex()
    r = requests.get("http://aes.cryptohack.org/ecb_oracle/encrypt/" + plain_hex)
    return r.json()['ciphertext']

def pad_func(guess):
    padding = "A" * (16 - len(guess) % 16)
    padded = padding + guess + padding
    return padded

def decrypt():
    letters = "abcdefghijklmnopqrstuvwxyz1234567890_{}"
    flag = ""

    while True:
        for letter in letters:
            flag_guess = flag + letter
            padded_guess = pad_func(flag_guess)
            ct = encrypt(padded_guess)

            guess_size = 2 * ((16 - len(flag_guess) % 16) + len(flag_guess))

            encrypted_guess = ct[:guess_size]
            encrypted_flag = ct[guess_size:guess_size*2]

            if encrypted_guess == encrypted_flag:
                flag = flag_guess
                print(flag)
                break
        if flag.endswith('}'): break  # flag format = crypto{}
    print()

decrypt()