from Crypto.Util.number import long_to_bytes
import numpy as np

def berlekamp_massey(sequence):
    """
    Thuật toán Berlekamp-Massey để tìm LFSR polynomial tối thiểu
    """
    n = len(sequence)
    c = [0] * n
    b = [0] * n
    c[0] = 1
    b[0] = 1
    L = 0
    m = -1
    
    for i in range(n):
        d = sequence[i]
        for j in range(1, L + 1):
            d ^= c[j] & sequence[i - j]
        
        if d == 1:
            temp = c[:]
            for j in range(len(b)):
                if i - m + j < len(c):
                    c[i - m + j] ^= b[j]
            
            if 2 * L <= i:
                L = i + 1 - L
                m = i
                b = temp
    
    taps = [i for i in range(1, L + 1) if c[i] == 1]
    return taps, L

def solve_lfsr_matrix(stream, state_len):
    """
    Giải LFSR bằng phương pháp ma trận tuyến tính
    Mỗi bit output phụ thuộc tuyến tính vào initial state
    """
    print("\n=== Solving using Linear Algebra ===")
    
    # Tìm taps trước
    taps, degree = berlekamp_massey(stream)
    print(f"LFSR degree: {degree}")
    print(f"Taps (1-indexed): {taps}")
    
    # Convert to 0-indexed
    tap_positions = [t - 1 for t in taps]
    
    # Xây dựng ma trận để biểu diễn quan hệ tuyến tính
    # stream[i] = f(initial_state) cho một hàm tuyến tính f
    
    # Với LFSR, sau khi clock 768 lần, mỗi output bit là XOR của một số bits từ initial state
    # Ta cần tạo một hệ phương trình tuyến tính
    
    num_clocks = 16 * 48  # 768 clocks trong __init__
    
    # Ma trận chuyển trạng thái (state transition matrix)
    # Mỗi lần clock: new_state = T * old_state (mod 2)
    T = np.zeros((state_len, state_len), dtype=int)
    
    # Xây dựng ma trận T
    # s' = [s[1], s[2], ..., s[n-1], c]
    # Trong đó c = s[tap_positions[0]] XOR s[tap_positions[1]] XOR ...
    
    for i in range(state_len - 1):
        T[i][i + 1] = 1  # s'[i] = s[i+1]
    
    # Bit cuối cùng là feedback
    for tap in tap_positions:
        T[state_len - 1][tap] = 1
    
    # Ma trận sau num_clocks lần clock: T^num_clocks
    print(f"Computing state transition matrix after {num_clocks} clocks...")
    T_power = matrix_power_mod2(T, num_clocks)
    
    # Vector output: bit đầu tiên của state sau mỗi clock
    # output[i] = e0^T * T^(768+i) * initial_state
    # Trong đó e0 = [1, 0, 0, ..., 0]
    
    e0 = np.zeros(state_len, dtype=int)
    e0[0] = 1
    
    # Xây dựng ma trận A: stream = A * initial_state (mod 2)
    A = np.zeros((len(stream), state_len), dtype=int)
    
    print("Building coefficient matrix...")
    current_T = T_power.copy()  # T^768
    
    for i in range(min(len(stream), state_len + 100)):
        if i % 100 == 0:
            print(f"Progress: {i}/{min(len(stream), state_len + 100)}")
        
        # stream[i] = first bit of (T^(768+i) * initial_state)
        # = e0^T * T^(768+i) * initial_state
        row = e0.dot(current_T) % 2
        A[i] = row
        
        # Update: T^(768+i+1) = T * T^(768+i)
        current_T = (T.dot(current_T)) % 2
    
    # Giải hệ phương trình: A * x = stream (mod 2)
    print("\nSolving linear system (mod 2)...")
    
    # Sử dụng Gaussian elimination trong GF(2)
    initial_state = gauss_eliminate_gf2(A[:state_len], stream[:state_len])
    
    return initial_state, tap_positions

def matrix_power_mod2(M, n):
    """Tính M^n (mod 2) bằng binary exponentiation"""
    size = M.shape[0]
    result = np.eye(size, dtype=int)
    base = M.copy()
    
    while n > 0:
        if n % 2 == 1:
            result = (result.dot(base)) % 2
        base = (base.dot(base)) % 2
        n //= 2
    
    return result

def gauss_eliminate_gf2(A, b):
    """
    Gaussian elimination trong GF(2)
    Giải Ax = b (mod 2)
    """
    A = A.copy()
    b = np.array(b, dtype=int).copy()
    m, n = A.shape
    
    # Augmented matrix
    aug = np.column_stack([A, b])
    
    # Forward elimination
    pivot_row = 0
    for col in range(n):
        # Tìm pivot
        found_pivot = False
        for row in range(pivot_row, m):
            if aug[row][col] == 1:
                # Swap rows
                aug[[pivot_row, row]] = aug[[row, pivot_row]]
                found_pivot = True
                break
        
        if not found_pivot:
            continue
        
        # Eliminate
        for row in range(m):
            if row != pivot_row and aug[row][col] == 1:
                aug[row] = (aug[row] + aug[pivot_row]) % 2
        
        pivot_row += 1
    
    # Back substitution
    x = np.zeros(n, dtype=int)
    for i in range(min(pivot_row, n) - 1, -1, -1):
        # Tìm leading 1
        leading_col = -1
        for j in range(n):
            if aug[i][j] == 1:
                leading_col = j
                break
        
        if leading_col == -1:
            continue
        
        x[leading_col] = aug[i][-1]
        for j in range(leading_col + 1, n):
            x[leading_col] ^= (aug[i][j] & x[j])
    
    return x.tolist()

def verify_solution(initial_state, tap_positions, num_clocks, expected_stream):
    """Verify solution"""
    state = initial_state[:]
    
    # Clock num_clocks times
    for _ in range(num_clocks):
        c = 0
        for t in tap_positions:
            c ^= state[t]
        state = state[1:] + [c]
    
    # Generate stream
    output = []
    verify_len = min(200, len(expected_stream))
    for _ in range(verify_len):
        b = state[0]
        output.append(b)
        c = 0
        for t in tap_positions:
            c ^= state[t]
        state = state[1:] + [c]
    
    matches = sum(1 for i in range(verify_len) if output[i] == expected_stream[i])
    print(f"\nVerification: {matches}/{verify_len} bits match")
    return matches == verify_len

# Main
stream_str = "00101101100100011101101110000000101100001110110001011110110011011011011011001111111101111101011111010000001011000011111010110011010111000100110010101100101000011000111010110011110011001001000101010010011100001011100101010000111100001010101001100010101110110110111000111010000011000000000010110101011011011111100100010100101100110000111010001101010111010010011110000110110010100010011101111111101001111101001100110110111110100101000010000000000010000000100100001110001110100001100111111010110010010110000000001110101101011001011011001101001010000000100010011001000100111000110100101011101001100110010110010011100010011101010000010101010001111110101010111001111000111111011011101011100011010101011010110001101110110101111001101110010100010110100100000000100000111000110010101100111111101001100111110000101011100111110010001111100000110110110110010101101110111100101010011000100110001000110011111110011110111001100110001011111111111011010010010110010011101011001010010101011001010100110001001111111000110011010101011011010110000101011011001100100000000000011111110101001100011001110000101110001101011011110000100111100010111110101101101010100110100010011001000110010100000001110010011001111110010001110110110100000001110110111011010100100111011011100001110100001110101111010100110101110100111111101100011010110011111111100011101110001111011100000000100110010111100100110100011000110110001001011111110000111001110010010111101000100011100101001111101011011011111011100011000001011011101111101111011011101011101110011011111001011101101100111111000000100000100011111101110100110100000111010001101100011000100000100010010111101111011000001011110101001010001000001001000111101110101001010110101101101010001110000001000001011110001011100011011010010110011011111111110010111101011111111101111110001100101001011010110001000001000111000101010100001000000101000100011100111001100111010010100101100100101001010100001100111001011111110011000000110000110101101000001110100101110011110001111000001111000100111000111011010100101000001101111100011011000111010001110110"

print("=== LFSR Decryption ===")
stream = [int(b) for b in stream_str]
print(f"Stream length: {len(stream)} bits")

try:
    initial_state, tap_positions = solve_lfsr_matrix(stream, 384)
    
    if initial_state:
        print("\n✓ Initial state recovered!")
        
        # Convert to bytes
        state_bits = ''.join(map(str, initial_state))
        state_int = int(state_bits, 2)
        flag_bytes = long_to_bytes(state_int)
        
        print(f"\nFlag (hex): {flag_bytes.hex()}")
        print(f"Flag (raw): {flag_bytes}")
        
        # Try to decode
        try:
            flag_text = flag_bytes.decode('ascii')
            print(f"Flag (ascii): {flag_text}")
        except:
            print("(Cannot decode as ASCII)")
        
        # Verify
        is_valid = verify_solution(initial_state, tap_positions, 768, stream)
        
        if is_valid:
            print("\n✓✓✓ VERIFICATION SUCCESSFUL! ✓✓✓")
            print(f"\nFINAL FLAG: {flag_bytes}")
        else:
            print("\n✗ Verification failed")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()