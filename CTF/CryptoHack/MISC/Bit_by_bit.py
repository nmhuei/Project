from Crypto.Random import random
from Crypto.Util.number import *

FLAG = b'crypto{??????????????????????????????????????????}'
q = 117477667918738952579183719876352811442282667176975299658506388983916794266542270944999203435163206062215810775822922421123910464455461286519153688505926472313006014806485076205663018026742480181999336912300022514436004673587192018846621666145334296696433207116469994110066128730623149834083870252895489152123
g = 104831378861792918406603185872102963672377675787070244288476520132867186367073243128721932355048896327567834691503031058630891431160772435946803430038048387919820523845278192892527138537973452950296897433212693740878617106403233353998322359462259883977147097970627584785653515124418036488904398507208057206926

pairs = []

with open("out.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for i in range(0, len(lines), 2):
    pk_line = lines[i].strip("()")
    c_line = lines[i+1].strip("()")
    pk_val = int(pk_line.split("=")[1], 16)
    c_parts = dict(x.split("=") for x in c_line.split(", "))
    pairs.append({
        "public_key": pk_val,
        "c1": int(c_parts["c1"], 16),
        "c2": int(c_parts["c2"], 16)
    })

def check_root(a, p=q):
    return pow(a, (p-1)//2, p)

s = ''
d = 0
for pair in pairs:
    h = pair["public_key"]
    c1 = pair["c1"]
    c2 = pair["c2"]
    
    if check_root(c2) == 1:
        s += '1'
        continue
    
    if check_root(c2) == -1 and check_root(c1) == -1 and check_root(h) == -1:
        d += 1
        
    s += '0'
    
    
print(long_to_bytes(int(s[::-1], 2)))
print(d)

