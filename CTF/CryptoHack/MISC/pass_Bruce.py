#!/usr/bin/env python3
from Crypto.Util.number import isPrime
import numpy as np
import itertools
import random
import time
import string

ALPHABET = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + "_")
odd_chars = [c for c in ALPHABET if ord(c) & 1]
lower_set = set(c for c in odd_chars if c.islower())
upper_set = set(c for c in odd_chars if c.isupper())
digit_set = set(c for c in odd_chars if c.isdigit())

def check(s):
    arr = np.array(list(map(ord, s)), dtype=np.int64)
    ssum, pprod = int(arr.sum()), int(arr.prod())
    if pprod <= 1:
        return False
    return isPrime(ssum) and isPrime(pprod)

def exhaustive(max_len=5):
    for n in range(3, max_len+1):
        print(f"Length {n}...")
        for tup in itertools.product(odd_chars, repeat=n):
            s = "".join(tup)
            if not (any(c in digit_set for c in s) and any(c in lower_set for c in s) and any(c in upper_set for c in s)):
                continue
            if check(s):
                return s
    return None

def randomized(timeout=300, max_tries=1000000):
    start = time.time()
    for tries in range(max_tries):
        if time.time() - start > timeout:
            break
        n = random.randint(3, 12)
        pos = list(range(n))
        random.shuffle(pos)
        s_list = [random.choice(odd_chars) for _ in range(n)]
        s_list[pos[0]] = random.choice(list(lower_set))
        s_list[pos[1]] = random.choice(list(upper_set))
        s_list[pos[2]] = random.choice(list(digit_set))
        if check("".join(s_list)):
            return "".join(s_list)
    return None

if __name__ == "__main__":
    result = exhaustive(5) or randomized(300, 2000000)
    print(f"Solution: {result}" if result else "No solution found")