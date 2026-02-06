#!/usr/bin/env python3
from pwn import remote

def to_bin_str(n):
    # positive integer -> binary without '0b'
    return bin(n)[2:]

def twos_complement(n, bits):
    mask = (1 << bits) - 1
    return bin(n & mask)[2:].rjust(bits, '0')

def pad_to_bits(binstr, bits):
    return binstr.rjust(bits, '0')

def parse_int_from_bin(s):
    return int(s, 2)

def detect_operator(op_line):
    """Return normalized operator and any operand index for unary ops (1 or 2 or None)."""
    t = op_line.strip().lower()
    # direct single-char ops
    if t in ['+', '-', '*', '^', '&', '|', '~']:
        mapping = {'+':'+','-':'-','*':'*','^':'^','&':'and','|':'or','~':'not'}
        return mapping[t], None

    # words
    if 'add' in t or t == 'plus' or '+' in t:
        return '+', None
    if 'minus' in t or 'sub' in t or '-' in t:
        return '-', None
    if 'mul' in t or 'times' in t or '*' in t:
        return '*', None
    if 'xor' in t or '^' in t:
        return '^', None
    if 'and' in t:
        return 'and', None
    if 'or' in t:
        return 'or', None
    if 'not' in t or t.startswith('~'):
        # check if mentions which operand: "not 2" or "not bn2" or "not bn 2"
        if '2' in t:
            return 'not', 2
        if '1' in t:
            return 'not', 1
        # default none -> apply to BN1
        return 'not', None

    # fallback: try to find symbols
    if '&' in t:
        return 'and', None
    if '|' in t:
        return 'or', None

    return None, None

def main():
    host = "titan.picoctf.net"
    port = 63336
    r = remote(host, port)

    # read BN1, BN2
    r.recvuntil(b'Binary Number 1: ')
    bn1_bin = r.recvline().decode().strip()
    r.recvuntil(b'Binary Number 2: ')
    bn2_bin = r.recvline().decode().strip()

    bn1 = parse_int_from_bin(bn1_bin)
    bn2 = parse_int_from_bin(bn2_bin)

    print("BN1:", bn1_bin, "=>", bn1)
    print("BN2:", bn2_bin, "=>", bn2)

    base_bits = max(len(bn1_bin), len(bn2_bin))
    last_result = None
    i = 1

    try:
        while True:
            prompt = f'Operation {i}: '.encode()
            r.recvuntil(prompt)
            op_line = r.recvline().decode().strip()
            if op_line == "":
                print("Empty operation line; breaking.")
                break

            operator, unary_target = detect_operator(op_line)

            if operator is None:
                print("Không xác định operator từ dòng:", op_line)
                # try to read remaining and break
                # print any remaining short line
                try:
                    extra = r.recvline(timeout=0.5)
                    if extra:
                        print("Extra:", extra.decode(errors='ignore'))
                except:
                    pass
                break

            # compute
            if operator == '+':
                res_val = bn1 + bn2
                res_bin = to_bin_str(res_val)
            elif operator == '-':
                res_val = bn1 - bn2
                if res_val < 0:
                    # gửi two's complement with base_bits
                    res_bin = twos_complement(res_val, base_bits)
                else:
                    res_bin = to_bin_str(res_val)
            elif operator == '*':
                res_val = bn1 * bn2
                res_bin = to_bin_str(res_val)
            elif operator == '^':
                res_val = bn1 ^ bn2
                res_bin = to_bin_str(res_val)
            elif operator == 'and':
                res_val = bn1 & bn2
                # we may want to show with base_bits padding
                res_bin = to_bin_str(res_val)
                # pad to base_bits to be safe
                res_bin = pad_to_bits(res_bin, base_bits)
            elif operator == 'or':
                res_val = bn1 | bn2
                res_bin = to_bin_str(res_val)
                res_bin = pad_to_bits(res_bin, base_bits)
            elif operator == 'not':
                # unary: determine operand
                if unary_target == 2:
                    operand = bn2
                elif unary_target == 1:
                    operand = bn1
                else:
                    # default apply to BN1
                    operand = bn1
                mask = (1 << base_bits) - 1
                res_val = (~operand) & mask
                res_bin = twos_complement(res_val, base_bits)
            else:
                print("Unhandled operator after parse:", operator)
                break

            last_result = res_val
            print(f"[{i}] {operator} -> {res_bin} (dec {res_val})")
            r.sendline(res_bin.encode())
            i += 1

    except EOFError:
        print("Remote closed (EOF).")
    except Exception as e:
        print("Exception:", e)

    # check leftover for hex/final prompt; if found, send last_result as hex
    try:
        rest = r.recv(timeout=1)
        if rest:
            txt = rest.decode(errors='ignore')
            print("Remaining:", txt)
            if ('hex' in txt.lower() or 'final' in txt.lower()) and last_result is not None:
                hex_str = format(last_result, 'x')
                print("Sending final hex:", hex_str)
                r.sendline(hex_str.encode())
    except Exception:
        pass

    r.interactive()

if __name__ == "__main__":
    main()
