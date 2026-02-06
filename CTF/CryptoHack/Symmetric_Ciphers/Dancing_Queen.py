from binascii import unhexlify


iv1 = 'e42758d6d218013ea63e3c49'
iv2 = 'a99f9a7d097daabd2aa2a235'
msg_enc = 'f3afbada8237af6e94c7d2065ee0e221a1748b8c7b11105a8cc8a1c74253611c94fe7ea6fa8a9133505772ef619f04b05d2e2b0732cc483df72ccebb09a92c211ef5a52628094f09a30fc692cb25647f'
flag_enc = 'b6327e9a2253034096344ad5694a2040b114753e24ea9c1af17c10263281fb0fe622b32732'
iv1 = bytes.fromhex(iv1)        # iv1 từ server
iv2 = bytes.fromhex(iv2)        # iv2 từ server
msg_enc = bytes.fromhex(msg_enc)    # msg_enc từ server
flag_enc = bytes.fromhex(flag_enc) 

msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# lấy keystream từ bản rõ đã biết
keystream = xor(msg, msg_enc[:len(msg)])

# giải mã flag
flag = xor(flag_enc[:len(keystream)], keystream)
print("Flag:", flag)