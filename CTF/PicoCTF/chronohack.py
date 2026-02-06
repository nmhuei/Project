from pwn import *
import random, time

def get_random(length, t):
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    random.seed(int(t*1000))
    return "".join(random.choice(alphabet) for _ in range(length))

p = remote("verbal-sleep.picoctf.net", 57751)
base = time.time()
for i in range(50):
    guess = get_random(20, base + i*0.001)
    p.recvuntil(b"):")
    p.sendline(guess.encode())
    line = p.recvline()
    if b"Congratulations" in line:
        print(p.recvline().decode())
        break