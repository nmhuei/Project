def S(a):
    return {
        p for p in range(3, 4*a + 1, 2)
        if kronecker_symbol(a, p) == -1
    }

def strong_pseudoprime(A, ks):
    x = var('x')
    def f(i):
        p = product(ks[j]*(x-1)+1 for j in range(len(ks)) if j != i)
        return (p - 1) / (x - 1)

    # subsets is dict that maps bases a_i to subsets of residues mod 4a
    subsets = {}
    for a in A:
        subsets[a] = list(set.intersection(*(
            {(pow(k, -1, 4*a) * (s + k - 1)) % (4*a) for s in S(a)}
            for k in ks
        )))

    indices = [0] * len(subsets)
    def bruteforce(i, r, m):
        if i == len(indices):
            yield find_pseudoprime(r, m)
            return

        for residue in subsets[A[i]]:
            try:
                r = crt([r, residue], [m, A[i] * 4])
            except ValueError:
                continue
            yield from bruteforce(i + 1, r, lcm(m, A[i] * 4))

    def find_pseudoprime(r, m):
        i = 0
        while True:
            p1 = m*i + r
            ps = [p1] + [
                k*(p1 - 1) + 1
                for k in ks[1:]
            ]
            if all(is_prime(p) for p in ps):
                return ps
            i += 1

    # initial congruences to ensure m_i is integer
    rs, ms = [], []
    for i in range(1, len(ks)):
        sol, = solve_mod(f(i).full_simplify(), ks[i])[0]
        rs.append(int(sol)); ms.append(ks[i])

    yield from bruteforce(0, crt(rs, ms), lcm(ms))

# USAGE
A = prime_range(2, 61+1)
for p in strong_pseudoprime(A, [1, 2081, 4177]):
    # assert miller_rabin(product(p), A)
    print(p)