# --- Input (theo đề bạn đưa) ---
p = 2^127 - 1
F.<i> = GF(p^2, modulus=[1,0,1])        # F_{p^2} với i^2 = -1
E = EllipticCurve(F, [1,0])              # y^2 = x^3 + x  (j=1728, supersingular)

P = E(24722427318870186874942502106037863239*i + 62223422355562631021732597235582046928,
      66881667812593541117238448140445071224*i + 149178354082347398743922440593055790802)
Q = E(136066972787979381470429160016223396048*i + 52082760150043245190232762320312239515,
      37290474751398918861353632929218878189*i + 89777436105166947842660822806860901885)
R = E(115434063687215369570994517493754451626*i + 158874018596958922133589852067300239562,
      62259011436032820287439957155108559928*i + 81253318200557694469168638082106161224)
S = E(42595488035799156418773068781330714859*i + 113049342376647649006990912915011269440,
      25404988689109287499485677343768857329*i + 125117346805247292256813555413193592812)

iv_hex = '6f5a901b9dc00aded4add3791812883b'
ct_hex = ('56ecb68a90cad9787a24a4511720d40d625901577f6d0f1eef9fc34cf0427091'
          '10cdc061fff91e934877674a30ed911283b83927dbcc270ae358d6b1fe2d5bed'
          '18ce1b02d8805de55e5b36deb0d28883')

# --- 1) Bậc của P,Q (thường là lũy thừa nhỏ của 2 hoặc 3) ---
nP = P.order()
nQ = Q.order()
print("ord(P) =", nP)
print("ord(Q) =", nQ)
if nP != nQ:
    n = lcm(nP, nQ)
else:
    n = nP
print("torsion n =", n)

# Kiểm tra R, S thuộc <P,Q>
assert (n*P).is_zero() and (n*Q).is_zero()
assert (n*R).is_zero() and (n*S).is_zero()

# --- 2) Weil pairing để lấy α, β sao cho R = αP + βQ ---
g = E.weil_pairing(P, Q, n)             # g = e_n(P,Q) (phần tử bậc n)
eRQ = E.weil_pairing(R, Q, n)           # = g^α
eRP = E.weil_pairing(R, P, n)           # = g^{-β}

# discrete log trong nhóm cyclic sinh bởi g
alpha = discrete_log(eRQ, g, ord=n)     # eRQ = g^alpha
beta  = (- discrete_log(eRP, g, ord=n)) % n  # eRP = g^{-beta}
print("alpha =", alpha)
print("beta  =", beta)

# (tuỳ bài: có thể đối chiếu với S)
# e(S,Q) ?= g^{?}, e(S,P) ?= g^{?}, dùng để sanity-check.

# --- 3) Hai cách lấy shared secret ---

# 3a) Pairing-based secret (rất hay gặp):
K_pair = g^(alpha*beta % n)             # thuộc μ_n ⊂ F_{p^2}*
print("K_pair =", K_pair)

# 3b) Point-based secret (nếu đề yêu cầu x-coordinate):
T = alpha*Q + beta*P
xT = T[0]
print("x(T) =", xT)

# Chọn 1 trong 2 để làm vật liệu khoá:
#   secret_bytes = K_pair.polynomial().coefficients() ... (chuyển về bytes)
# Hoặc đơn giản: dùng repr() / to_bytes nhất quán:

def Felt_to_bytes(z):
    # z = a + b*i in F_{p^2}
    a = int(z.polynomial().coefficients()[0]) if z != 0 else 0
    b = int((z - a).polynomial().coefficients()[0]) if z != 0 else 0  # cách nhanh gọn
    # ghép a||b với độ dài cố định (16 bytes cho p≈2^127), little/big tuỳ bạn
    return a.to_bytes(16, 'big') + b.to_bytes(16, 'big')

secret_bytes = Felt_to_bytes(K_pair)    # hoặc Felt_to_bytes(xT) nếu dùng điểm

# --- 4) Derive key & AES-CBC decrypt ---
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = hashlib.sha256(secret_bytes).digest()
iv  = bytes.fromhex(iv_hex)
ct  = bytes.fromhex(ct_hex)

cipher = AES.new(key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), AES.block_size)
print("PLAINTEXT =", pt)
