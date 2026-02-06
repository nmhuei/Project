# field
p = 4368590184733545720227961182704359358435747188309319510520316493183539079703
F = GF(p)

# base point
gx = 8742397231329873984594235438374590234800923467289367269837473862487362482
gy = 225987949353410341392975247044711665782695329311463646299187580326445253608

# public point
px = 2582928974243465355371953056699793745022552378548418288211138499777818633265
py = 2421683573446497972507172385881793260176370025964652384676141384239699096612

# two points are enough to recover the curve parameters
M = Matrix(F, [[gx,1],[px,1]])
a,b = M.solve_right(vector([gy^2-gx^3,py^2-px^3]))

# that's not an elliptic curve!
assert 4*a^3 + 27*b^2 == 0

# finding the roots, here we suppose the singular point is a node
# we make sure alpha is the double root
K.<x> = F[]
f = x^3 + a*x + b
roots = f.roots()
if roots[0][1] == 1:
    beta, alpha = roots[0][0], roots[1][0]
else:
    alpha, beta = roots[0][0], roots[1][0]

# transfer
slope = (alpha - beta).sqrt()
u = (gy + slope*(gx-alpha))/(gy - slope*(gx-alpha))
v = (py + slope*(px-alpha))/(py - slope*(px-alpha))

# should take a few seconds, don't worry (largest prime of p-1 is 42 bits only)
flag = discrete_log(v, u)
print(int.to_bytes(int(flag), (flag.nbits()+7)//8, 'big').decode())