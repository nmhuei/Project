from Crypto.PublicKey import RSA

with open("transparency.pem", 'r') as f:
    key = RSA.import_key(f.read())
    
print("Modulus (n):", key.n)
print("Public exponent (e):", key.e)