import base64, struct

def read_mpint(blob, offset):
    """Đọc 1 số nguyên đa-precision (mpint)"""
    ln = struct.unpack(">I", blob[offset:offset+4])[0]
    offset += 4
    val = int.from_bytes(blob[offset:offset+ln], "big")
    offset += ln
    return val, offset

def parse_ssh_rsa_pub(filename):
    with open(filename, "r") as f:
        parts = f.read().strip().split()
        keytype, b64data = parts[0], parts[1]
        comment = parts[2] if len(parts) > 2 else ""
        if keytype != "ssh-rsa":
            raise ValueError("Không phải khóa ssh-rsa")
    blob = base64.b64decode(b64data)

    # đọc "ssh-rsa"
    off = 0
    l = struct.unpack(">I", blob[off:off+4])[0]; off += 4
    assert blob[off:off+l] == b"ssh-rsa"; off += l

    e, off = read_mpint(blob, off)  # public exponent
    n, off = read_mpint(blob, off)  # modulus

    return {"e": e, "n": n, "bits": n.bit_length(), "comment": comment}

if __name__ == "__main__":
    info = parse_ssh_rsa_pub("key-rsa.pub")
    print("Comment:", info["comment"])
    print("Exponent e:", info["e"])
    print("Modulus n (hex):", int(info["n"]))
    print("Key size:", info["bits"], "bits")
