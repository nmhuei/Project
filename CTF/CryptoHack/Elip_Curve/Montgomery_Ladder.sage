
from sage.all import GF,EllipticCurve

p = (2**255) - 19
# create a finite field 
F = GF(p)
# y^2 + a_1 xy + a_3 y = x^3 + a_2 x^2 + a_4 x + a_6
E = EllipticCurve(F, [0,486662,0,1,0])

G_x = F(9)
G = E.lift_x(G_x)
k = 0x1337c0decafe
Q = k*G

print(f"crypto{{{Q.xy()[0]}}}")