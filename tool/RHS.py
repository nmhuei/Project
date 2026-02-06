from Crypto.Util.number import isPrime

def legendre_symbol(a, p):
    """Tính ký hiệu Legendre (a|p), p là số nguyên tố lẻ"""
    return pow(a, (p - 1) // 2, p)

def mod_sqrt(a, p):
    """
    Tìm căn bậc hai của a mod p (p nguyên tố lẻ).
    Trả về tuple (r, p-r) nếu có nghiệm, None nếu không tồn tại.
    """
    if a == 0:
        return (0, 0)
    if p == 2:
        return (a, a)
    
    # kiểm tra xem a có là quadratic residue không
    if legendre_symbol(a, p) != 1:
        return None
    
    # Trường hợp nhanh: p ≡ 3 mod 4
    if p % 4 == 3:
        r = pow(a, (p + 1) // 4, p)
        return (r, p - r)
    
    # Trường hợp p ≡ 1 mod 4 → dùng Tonelli-Shanks
    # B1: viết p-1 = q * 2^s với q lẻ
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    
    # B2: tìm z là quadratic non-residue mod p
    z = 2
    while legendre_symbol(z, p) != p - 1:
        z += 1
    
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    
    while t != 1:
        # tìm số mũ i nhỏ nhất sao cho t^(2^i) ≡ 1 mod p
        i = 1
        t2i = pow(t, 2, p)
        while t2i != 1:
            t2i = pow(t2i, 2, p)
            i += 1
            if i == m:
                return None  # không có nghiệm
        
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b * b) % p
        r = (r * b) % p
        t = (t * c) % p
    
    return (r, p - r)

a = 4
p = 2**255 - 19

print(mod_sqrt(a, p))
