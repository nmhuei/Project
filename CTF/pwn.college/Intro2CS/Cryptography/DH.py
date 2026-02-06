import requests, re, base64, string

url = 'http://challenge.localhost/'

# regex cho base64 trong <pre> ... </pre>
RE_CT = re.compile(r"<b>Encrypted backup:</b>\s*<pre>\s*([A-Za-z0-9+/=]+)\s*</pre>", re.I|re.S)

def pad(s):
    pad_len = (16 - len(s)) % 16
    padding = '|' * pad_len
    padded = padding + s + padding
    return padded, (len(padded) - pad_len) * 2

def get_ct(content: str) -> str:
    # thêm content
    requests.post(url, data={'content': content})
    # lấy trang để đọc ciphertext base64
    r = requests.get(url)
    m = RE_CT.search(r.text)
    if not m:
        raise ValueError("Không tìm thấy ciphertext trong response!")
    ct_b64 = m.group(1).strip()
    # reset DB để chỉ còn flag
    requests.post(url + 'reset')
    return base64.b64decode(ct_b64).hex()


flag = '|pwn.college{'
charset = '{_}.-' + string.digits + string.ascii_uppercase + string.ascii_lowercase 

while not flag.endswith('}'):

    Found = False

    for c in charset:
        flag_guess = flag + c
        flag_guess_pad, flag_guess_len = pad(flag_guess)
        flag_guess_encrypted = get_ct(flag_guess_pad)

        if flag_guess_encrypted[:flag_guess_len] == flag_guess_encrypted[flag_guess_len:flag_guess_len*2]:

            