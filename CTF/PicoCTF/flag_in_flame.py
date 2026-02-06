import base64

with open("logs.txt", 'r') as f:
    data = f.read()
    
with open("output.jpg", "wb") as f:
    f.write(base64.b64decode(data))