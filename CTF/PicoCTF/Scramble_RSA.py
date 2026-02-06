import string

from pwn import*
from Crypto.Util.number import*
context.log_level = "error"

HOST, POST = "mercury.picoctf.net", 47987

def remove_duplicates_keep_order(s: str) -> str:
    result = ""
    seen = set()
    for ch in s:
        if ch not in seen:
            result += ch
            seen.add(ch)
    return result

r = remote(HOST, POST)

flag = r.recvline().strip().split()[1].decode()

character = "0123456789picoCTF}{bad_1d3a_abdefghjklmnprstuvwxyzABDEGHIJKLMNOPQRSUVWXYZ"
character = remove_duplicates_keep_order(character)

solution = ''
flag_encrypt = []
while True:
    Found = False
    if flag.endswith('}'):
        print('[*] Here is your flag:',flag)
        
    for c in character:
        guess = c
        flag_guess = solution + c
        
        r.recvuntil(b'I will encrypt whatever you give me:')
        r.sendline(flag_guess.encode())
        flag_guess_encrypt = r.recvline().strip().split()[-1].decode()
        for character_encrypt in flag_encrypt:
            flag_guess_encrypt = flag_guess_encrypt.replace(character_encrypt, '')
            
            
        if flag_guess_encrypt in flag:
            flag_encrypt.append(flag_guess_encrypt)
            solution += c
            print('[*] Flag so far .... ', solution)
            Found = True
            break
            
    if Found == False:
        print("[*] FAILED")
        exit
        
    
        






