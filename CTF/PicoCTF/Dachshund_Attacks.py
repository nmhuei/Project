from fractions import Fraction
from math import isqrt
from Crypto.Util.number import *

def cont_frac_expansion(num, den):
    # Trả về các phần tử [a0, a1, a2, ...] của phân số liên tục num/den
    a = []
    while den:
        q = num // den
        a.append(q)
        num, den = den, num - q*den
    return a

def convergents(a):
    # Từ danh sách hệ số continued fraction -> dãy convergents (k/d)
    conv = []
    for i in range(1, len(a)+1):
        frac = Fraction(0, 1)
        for x in reversed(a[:i]):
            if frac.numerator == 0:
                frac = Fraction(x, 1)
            else:
                frac = x + Fraction(1, frac)
        conv.append(frac)  # k/d
    return conv

def wiener_attack(e, n):
    cf = cont_frac_expansion(e, n)
    for frac in convergents(cf):
        k, d = frac.numerator, frac.denominator
        if k == 0: 
            continue
        # phi_candidate = (e*d - 1) / k  phải nguyên
        ed_minus_1 = e*d - 1
        if ed_minus_1 % k != 0:
            continue
        phi = ed_minus_1 // k

        # Giải phương trình x^2 - (n - phi + 1)x + n = 0
        s = n - phi + 1
        delta = s*s - 4*n
        if delta < 0:
            continue
        t = isqrt(delta)
        if t*t != delta:
            continue
        # p,q nguyên
        p = (s + t) // 2
        q = (s - t) // 2
        if p*q == n and p > 1 and q > 1:
            return d, (p, q)
    return None, None

# Ví dụ dùng:
# e, n = ...  # thay bằng RSA public key của bạn
# d, (p,q) = wiener_attack(e, n)
# if d: print("Recovered d =", d)

e = 4205276770177167622514116229372160106449454933880958806307008193774550256685642820961379759208675143550545639870416577974244629230977731151379052375860155724748685596755565849175136855926922242219657282880349559087243723281259012800539001663607081775677832951984763314984536845290451593042281432140483664503
n = 88907588122435650575965658818349919869143159766927097000206139289463246410725247608121884727774619797203238242320615623498675535438249326234937467091467459986048273776317122895996788060845838358094450066329731564792226358838790716940470388639892930660571159383635068067073900913352691176221552109121548532459
c = 46176947140651942128629997178745788377086046457211675635681471826735773070934166340098780994599851957804009674346635709441265921830275882514535203226931882110310904780868648989317389733677478533837319969137475111158367918494790108636694538365387664889970581258156266236918421878055747062522461082989878114580

d, (p, q) = wiener_attack(e, n)
if d:
    print(long_to_bytes(pow(c, d, n)))
else:
    print('Attack Failed')
