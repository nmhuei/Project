def generator(g, x, p):
    return pow(g, x) % p

def encrypt(plaintext, key):
    cipher = []
    for char in plaintext:
        cipher.append(((ord(char) * key*311)))
    return cipher

def decrypt(cipher, key):
    plain = ''
    for char in cipher:
        plain += chr(char // key // 311)
    return plain

def dynamic_xor_encrypt(plaintext, text_key):
    cipher_text = ""
    key_length = len(text_key)
    for i, char in enumerate(plaintext[::-1]):
        key_char = text_key[i % key_length]
        encrypted_char = chr(ord(char) ^ ord(key_char))
        cipher_text += encrypted_char
    return cipher_text

def dynamic_xor_decrypt(ciphertext, text_key='trudeau'):
    key_length = len(text_key)
    tmp = []
    for i, char in enumerate(ciphertext):
        key_char = text_key[i % key_length]
        tmp.append(chr(ord(char) ^ ord(key_char)))
    return ''.join(tmp[::-1])

        
a = 95
b = 21
cipher = [237915, 1850450, 1850450, 158610, 2458455, 2273410, 1744710, 1744710, 1797580, 1110270, 0, 2194105, 555135, 132175, 1797580, 0, 581570, 2273410, 26435, 1638970, 634440, 713745, 158610, 158610, 449395, 158610, 687310, 1348185, 845920, 1295315, 687310, 185045, 317220, 449395]
p = 97
g = 31
u = generator(g, a, p)
v = generator(g, b, p)
key = generator(v, a, p)
b_key = generator(u, b, p)
shared_key = None
if key == b_key:
    shared_key = key
else:
    print("Invalid key")
    exit


semi_plain = decrypt(cipher, shared_key)
plain = dynamic_xor_decrypt(semi_plain)

print(plain)


