#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import *

context.log_level = "DEBUG"
# --- RSA public (chỉ để verify local nếu muốn) ---
N = 22266616657574989868109324252160663470925207690694094953312891282341426880506924648525181014287214350136557941201445475540830225059514652125310445352175047408966028497316806142156338927162621004774769949534239479839334209147097793526879762417526445739552772039876568156469224491682030314994880247983332964121759307658270083947005466578077153185206199759569902810832114058818478518470715726064960617482910172035743003538122402440142861494899725720505181663738931151677884218457824676140190841393217857683627886497104915390385283364971133316672332846071665082777884028170668140862010444247560019193505999704028222347577
E = 3

# --- ta muốn verified_vote kết thúc bằng b'\x00VOTE FOR PEDRO' ---
SUFFIX = b"\x00VOTE FOR PEDRO"   # độ dài 15 bytes
L = len(SUFFIX)
T = int.from_bytes(SUFFIX, "big")    # mục tiêu modulo 256^L
BASE = 256

def craft_cube_root_suffix(T: int, L: int) -> int:
    """
    Tìm S sao cho S^3 ≡ T (mod 256^L) bằng cách dựng dần từng byte:
        s -> s + 256^i * k_i
    với 3*s^2 invertible mod 256 (đảm bảo s lẻ).
    Trả về S trong khoảng [0, 256^L).
    """
    # B1: chọn s (1 byte) lẻ sao cho s^3 ≡ T (mod 256)
    t0 = T & 0xFF
    s = None
    for cand in range(1, 256, 2):         # chỉ thử số lẻ để 3*s^2 có nghịch đảo mod 256
        if (cand * cand * cand) % 256 == t0:
            s = cand
            break
    if s is None:
        raise ValueError("No 1-byte seed found (unexpected).")

    # B2: nâng dần lên 256^(i+1) với i = 1..L-1
    base_i = BASE  # 256^1
    for i in range(1, L):
        mod_i1 = base_i * BASE  # 256^(i+1)
        # delta = (T - s^3) mod 256^(i+1)
        delta = (T - pow(s, 3, mod_i1)) % mod_i1
        # tuyến tính: (s + base_i*k)^3 ≡ s^3 + 3*s^2*base_i*k (mod 256^(i+1))
        # Chia cả hai vế cho base_i (hợp lệ vì delta luôn là bội của base_i ở bước nâng):
        rhs = (delta // base_i) % 256
        a = (3 * (s * s % 256)) % 256       # 3*s^2 mod 256
        inv = pow(a, -1, 256)               # nghịch đảo mod 256 (được vì a lẻ)
        k = (rhs * inv) % 256
        s = s + base_i * k
        base_i *= BASE

    # bây giờ s^3 ≡ T (mod 256^L)
    return s % (BASE ** L)

def main():
    S = craft_cube_root_suffix(T, L)
    # Kiểm tra offline: S^3 có đúng kết thúc bằng \x00VOTE FOR PEDRO không?
    B = pow(S, 3)
    tail = long_to_bytes(B)[-L:] if len(long_to_bytes(B)) >= L else long_to_bytes(B).rjust(L, b"\x00")[-L:]
    assert tail == SUFFIX, "Tail check failed!"
    # Đồng thời B << N nên mod N không đổi:
    assert B < N

    # Gửi lên server
    HOST, PORT = "socket.cryptohack.org", 13375
    r = remote(HOST, PORT)
    r.recvuntil(b"Place your vote. Pedro offers a reward to anyone who votes for him!\n")
    payload = {"option": "vote", "vote": hex(S)}  # server: int(...,16)
    import json
    r.sendline(json.dumps(payload).encode())
    print(r.recvline().decode().strip())

if __name__ == "__main__":
    main()
