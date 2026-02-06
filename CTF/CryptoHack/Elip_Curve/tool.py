from Crypto.Util.number import*

p = 163
A = 145 
B = 49
jE = 1728*4*(A**3)*inverse(4*(A**3) + 27*(B**2), p) % p

print(jE)