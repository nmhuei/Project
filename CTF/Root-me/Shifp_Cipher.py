import re

with open("private.dump") as f:
    data = f.read()

# chỉ giữ lại hex
hexdata = re.sub(r'[^0-9a-fA-F]', '', data)

with open("private.bin", "wb") as f:
    f.write(bytes.fromhex(hexdata))

print("Wrote", len(hexdata)//2, "bytes to private.bin")
