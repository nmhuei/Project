from pwn import *
import json

# 2^128 collision protection!
BLOCK_SIZE = 32

# Nothing up my sleeve numbers (ref: Dual_EC_DRBG P-256 coordinates)
W = [0x6b17d1f2, 0xe12c4247, 0xf8bce6e5, 0x63a440f2, 0x77037d81, 0x2deb33a0, 0xf4a13945, 0xd898c296]
X = [0x4fe342e2, 0xfe1a7f9b, 0x8ee7eb4a, 0x7c0f9e16, 0x2bce3357, 0x6b315ece, 0xcbb64068, 0x37bf51f5]
Y = [0xc97445f4, 0x5cdef9f0, 0xd3e05e1e, 0x585fc297, 0x235b82b5, 0xbe8ff3ef, 0xca67c598, 0x52018192]
Z = [0xb28ef557, 0xba31dfcb, 0xdd21ac46, 0xe2a91e3c, 0x304f44cb, 0x87058ada, 0x2cb81515, 0x1e610046]

# Lets work with bytes instead!
W_bytes = b''.join([x.to_bytes(4,'big') for x in W])
X_bytes = b''.join([x.to_bytes(4,'big') for x in X])
Y_bytes = b''.join([x.to_bytes(4,'big') for x in Y])
Z_bytes = b''.join([x.to_bytes(4,'big') for x in Z])
print(W_bytes.hex())
print(X_bytes.hex())
print(Y_bytes.hex())
print(Z_bytes.hex())

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len]*padding_len)

def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def rotate_left(data, x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]

def rotate_right(data, x):
    x = x % BLOCK_SIZE
    return  data[-x:] + data[:-x]

def scramble_block(block):
    for _ in range(40):
        block = xor(W_bytes, block)
        block = rotate_left(block, 6)
        block = xor(X_bytes, block)
        block = rotate_right(block, 17)
    return block

def cryptohash(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)
    for i,b in enumerate(msg_blocks):
        mix_in = scramble_block(b)
        for _ in range(i):
            mix_in = rotate_right(mix_in, i+11)
            mix_in = xor(mix_in, X_bytes)
            mix_in = rotate_left(mix_in, i+6)
        initial_state = xor(initial_state,mix_in)
    return initial_state.hex()


# sử dụng các hàm của bạn: rotate_left, rotate_right, scramble_block, cryptohash, BLOCK_SIZE, etc.

def L_linear_rotation_amount(i):
    # r_i = 24 + 5*i  (mod 32 bytes)
    return (24 + 5 * i) % BLOCK_SIZE

def L_apply(i, block):
    # phần tuyến tính L_i(b) = rotate_right(block, r_i)
    # (theo phân tích, scramble_linear = rotate_right(24), và extra rotations => tổng r_i)
    # NOTE: vì scramble_block có affine offset, nhưng phần tuyến tính xử lý bằng rotate
    r = L_linear_rotation_amount(i)
    return rotate_right(block, r)

def make_collision_two_block(b0=None, b1=None, b0_prime=None):
    import os
    if b0 is None:
        b0 = os.urandom(BLOCK_SIZE)
    if b1 is None:
        b1 = os.urandom(BLOCK_SIZE)
    if b0_prime is None:
        # pick different random b0'
        while True:
            cand = os.urandom(BLOCK_SIZE)
            if cand != b0:
                b0_prime = cand
                break

    # i for first block = 0, for second block = 1 (as in your cryptohash loop)
    L0_b0  = L_apply(0, b0)
    L0_b0p = L_apply(0, b0_prime)
    L1_b1  = L_apply(1, b1)

    # rhs = L1(b1) xor L0(b0) xor L0(b0')
    rhs = bytes([x ^ y ^ z for x,y,z in zip(L1_b1, L0_b0, L0_b0p)])

    # invert L1: rotate left by r1
    r1 = L_linear_rotation_amount(1)
    # inverse of rotate_right(r1) is rotate_left(r1)
    b1_prime = rotate_left(rhs, r1)

    return (b0, b1, b0_prime, b1_prime)


# Example usage:
b0, b1, b0p, b1p = make_collision_two_block()
m1 = b0 + b1
m2 = b0p + b1p

r = remote("socket.cryptohack.org", 13405)
payload = {
    "m1": m1.hex(),
    "m2": m2.hex()
}

r.sendlineafter(
    b'Please send two hex encoded messages m1, m2 formatted in JSON: ', 
    json.dumps(payload).encode()
)

print(r.recvall(timeout=2))