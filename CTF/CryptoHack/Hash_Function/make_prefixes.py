#!/usr/bin/env python3
"""
make_prefixes.py
Generate a bunch of prefix .bin files (big-endian bytes, same format as long_to_bytes)
for use with chosen-prefix MD5 experiments. DOES NOT create collisions.
Usage:
  python3 make_prefixes.py --outdir ./prefixes --mode mixed --count 5 --sizes 32 48 64 96 128
"""

import os
import argparse
import secrets
from Crypto.Util.number import long_to_bytes, getPrime, isPrime

# small primes for quick sieve
def small_primes_upto(n=5000):
    sieve = bytearray(b'\x01') * (n+1)
    sieve[0:2] = b'\x00\x00'
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n+1:step] = b'\x00' * (((n - start)//step) + 1)
    return [i for i, v in enumerate(sieve) if v and i >= 2]

SMALL_PRIMES = small_primes_upto(2000)

def passes_small_sieve(n):
    for p in SMALL_PRIMES:
        if n % p == 0:
            return False, p
    return True, None

def make_prime_prefix(bits):
    # generate a prime of given bit length
    p = getPrime(bits)
    return p

def make_random_prefix(bits):
    # random odd integer of given bit length, ensure not divisible by small primes
    assert bits >= 8
    while True:
        n = secrets.randbits(bits - 1)  # ensure top bit maybe zero, we'll set top bit
        n |= (1 << (bits - 1))  # set MSB to ensure exact bit length
        n |= 1  # ensure odd
        # avoid trivial last byte 0x00 to keep suffix freedom
        if (n & 0xff) == 0:
            n |= 1
        ok, div = passes_small_sieve(n)
        if ok:
            return n

def write_prefix(n, outpath):
    b = long_to_bytes(n)
    with open(outpath, "wb") as f:
        f.write(b)
    return len(b), b.hex()[:64]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", "-o", default="./prefixes", help="output directory")
    p.add_argument("--mode", "-m", choices=("prime", "random", "mixed"), default="mixed",
                   help="type of prefixes to generate")
    p.add_argument("--count", "-c", type=int, default=5, help="number of prefixes per size")
    p.add_argument("--sizes", "-s", type=int, nargs="+", default=[32,48,64,96,128],
                   help="list of bit sizes for prefixes")
    p.add_argument("--sieve", type=int, default=2000, help="limit for small-prime sieve (default 2000)")
    args = p.parse_args()

    global SMALL_PRIMES
    SMALL_PRIMES = small_primes_upto(args.sieve)

    os.makedirs(args.outdir, exist_ok=True)
    created = []

    for bits in args.sizes:
        for i in range(args.count):
            if args.mode == "prime":
                n = make_prime_prefix(bits)
                tag = "prime"
            elif args.mode == "random":
                n = make_random_prefix(bits)
                tag = "rand"
            else:  # mixed
                # alternate prime and random to get variety
                if i % 2 == 0:
                    n = make_prime_prefix(bits)
                    tag = "prime"
                else:
                    n = make_random_prefix(bits)
                    tag = "rand"

            fname = f"prefix_{bits}b_{tag}_{i+1}.bin"
            outpath = os.path.join(args.outdir, fname)
            bytelen, hextail = write_prefix(n, outpath)
            created.append((outpath, bits, tag, n.bit_length(), bytelen, hextail))
            print(f"Created {outpath}: bits={n.bit_length()}, bytes={bytelen}, type={tag}")

    print("\nSummary:")
    for c in created:
        print(f" - {os.path.basename(c[0])}  ({c[1]} bits, {c[2]})")

    print(f"\nWrote {len(created)} prefix files into {args.outdir}")
    print("Now you can use these files as 'prefixA.bin' or 'prefixB.bin' in your offline hashclash runs.")
    print("Reminder: this script does NOT create collisions; run your chosen-prefix tool separately and then use these prefixes.")

if __name__ == "__main__":
    main()
