from Crypto.Util.number import long_to_bytes

def wiener(e, n):
    # Convert e/n into a continued fraction
    cf = continued_fraction(e/n)
    convergents = cf.convergents()
    for kd in convergents:
        k = kd.numerator()
        d = kd.denominator()
        # Check if k and d meet the requirements
        if k == 0 or d%2 == 0 or e*d % k != 1:
            continue
        phi = (e*d - 1)/k
        # Create the polynomial
        x = PolynomialRing(RationalField(), 'x').gen()
        f = x^2 - (n-phi+1)*x + n
        roots = f.roots()
        # Check if polynomial as two roots
        if len(roots) != 2:
            continue
        # Check if roots of the polynomial are p and q
        p,q = int(roots[0][0]), int(roots[1][0])
        if p*q == n:
            return d
    return None

e = 457712204773211845842589825458648687789148735588729042110512833559935097619490125097062943341079550973888839036890853874940140999770038586264697394249941373575612387145457162686771087729945257708865500160218092670137796904240536417183578020075663238772069915557909855816767797388962490189013648158592853773
N = 54460358444640918690694246877845440243188504768616558829847443570637150084751716866515743145977139433222414088108750199479937779747431095643042972338311643401234557475035967555946663151476461682519578941356676068053035637480135841854036672777878713952760267692026807631111466131434443590476494803803467637133
data = wiener(e, N)
print(data)