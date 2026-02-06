#!/usr/bin/env python3
"""
Phiên bản tối ưu cực mạnh - xử lý file cực lớn
Sử dụng thuật toán Newton's divided differences thay vì Vandermonde
"""

import numpy as np
import sys
import time
import os

# Simple progress function
def progress_bar(iterable, desc="Progress", total=None):
    """Simple progress display without tqdm"""
    if total is None:
        total = len(iterable)
    
    for i, item in enumerate(iterable):
        if i % max(1, total // 100) == 0 or i == total - 1:
            percent = (i + 1) / total * 100
            bar_len = 40
            filled = int(bar_len * (i + 1) / total)
            bar = '█' * filled + '-' * (bar_len - filled)
            print(f'\r{desc}: |{bar}| {percent:.1f}% ({i+1}/{total})', end='', flush=True)
        yield item
    print()  # New line after completion

MOD = 7514777789

def decode_ultra(input_file='encoded.txt', output_file='output.bmp', max_degree=1000):
    """
    Giải mã siêu tối ưu cho file cực lớn
    
    Chiến lược:
    1. Chỉ cần (degree + 1) điểm để khôi phục đa thức bậc degree
    2. Thường degree ≈ kích thước file gốc
    3. Sử dụng Newton's divided differences - O(n²) time, O(n) space
    
    Args:
        input_file: File đầu vào
        output_file: File đầu ra
        max_degree: Bậc tối đa của đa thức (tự động điều chỉnh)
    """
    print("🚀 BẮT ĐẦU GIẢI MÃ (Ultra-Optimized Mode)")
    print("=" * 60)
    
    # Kiểm tra file
    if not os.path.exists(input_file):
        print(f"❌ File '{input_file}' không tồn tại!")
        sys.exit(1)
    
    file_size_mb = os.path.getsize(input_file) / (1024 * 1024)
    print(f"📁 Kích thước file: {file_size_mb:.2f} MB")
    
    # Đếm số dòng
    print("📊 Đang đếm số điểm...")
    with open(input_file, 'r') as f:
        total_lines = sum(1 for _ in f)
    
    print(f"🔢 Tổng số điểm: {total_lines}")
    
    # Ước tính degree từ kích thước file
    # File BMP thường có header ~54 bytes, phần còn lại là pixel data
    estimated_file_size = int(file_size_mb * 1024)  # KB
    estimated_degree = estimated_file_size  # Rough estimate
    
    # Điều chỉnh số điểm cần đọc
    # Cần ít nhất (degree + 1) điểm, nhưng nên lấy thêm để an toàn
    safety_factor = 1.5
    points_needed = min(int(estimated_degree * safety_factor), max_degree)
    points_needed = max(points_needed, 100)  # Ít nhất 100 điểm
    points_needed = min(points_needed, total_lines)  # Không vượt quá số điểm có sẵn
    
    print(f"📐 Ước tính bậc đa thức: ~{estimated_degree}")
    print(f"📊 Số điểm sẽ đọc: {points_needed} ({points_needed/total_lines*100:.2f}%)")
    
    # Đọc dữ liệu
    print("\n📥 Đang đọc dữ liệu...")
    x_vals = []
    y_vals = []
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Chọn đều các điểm
    step = max(1, total_lines // points_needed)
    indices = list(range(0, total_lines, step))[:points_needed]
    
    print(f"   Chọn mỗi {step} điểm")
    
    for idx in progress_bar(indices, desc="Đọc điểm", total=len(indices)):
        line = lines[idx].strip()
        if line:
            parts = line.split()
            if len(parts) == 2:
                x_vals.append(int(parts[0]))
                y_vals.append(int(parts[1]))
    
    n = len(x_vals)
    print(f"✅ Đã đọc {n} điểm")
    
    # Tính hệ số bằng Newton's divided differences
    print("\n🧮 Đang tính hệ số đa thức (Newton's method)...")
    start_time = time.time()
    
    coeffs = newton_interpolation(x_vals, y_vals)
    
    end_time = time.time()
    print(f"⏱️  Thời gian tính toán: {end_time - start_time:.2f} giây")
    
    # Chuyển đổi sang dạng chuẩn (monomial basis)
    print("🔄 Đang chuyển đổi sang dạng chuẩn...")
    standard_coeffs = newton_to_standard(x_vals, coeffs)
    
    # Ghi file
    print(f"\n💾 Đang ghi file: {output_file}")
    with open(output_file, 'wb') as f:
        for i in progress_bar(range(len(standard_coeffs)), desc="Ghi byte", total=len(standard_coeffs)):
            byte_val = int(round(standard_coeffs[i])) % 256
            f.write(bytes([byte_val]))
    
    output_size_kb = os.path.getsize(output_file) / 1024
    print(f"✅ Đã ghi {len(standard_coeffs)} bytes ({output_size_kb:.2f} KB)")
    
    print("\n🎉 HOÀN THÀNH!")
    
    return standard_coeffs


def newton_interpolation(x_vals, y_vals):
    """
    Newton's divided differences
    O(n²) time, O(n) space - không cần ma trận lớn!
    """
    n = len(x_vals)
    
    # Bảng divided differences
    # Chỉ cần lưu 2 cột tại một thời điểm
    F = np.array(y_vals, dtype=np.float64)
    coeffs = [F[0]]
    
    for i in progress_bar(range(1, n), desc="Newton's differences", total=n-1):
        # Tính cột thứ i của bảng divided differences
        for j in range(n - i):
            F[j] = (F[j + 1] - F[j]) / (x_vals[j + i] - x_vals[j])
        
        coeffs.append(F[0])
    
    return coeffs


def newton_to_standard(x_vals, newton_coeffs):
    """
    Chuyển từ Newton form sang standard form (monomial basis)
    
    Newton form: c₀ + c₁(x-x₀) + c₂(x-x₀)(x-x₁) + ...
    Standard form: a₀ + a₁x + a₂x² + ...
    """
    n = len(newton_coeffs)
    
    # Bắt đầu với c₀
    result = np.zeros(n, dtype=np.float64)
    result[0] = newton_coeffs[0]
    
    # Tích lũy từng term
    current_poly = np.array([1.0], dtype=np.float64)  # Bắt đầu với 1
    
    for i in progress_bar(range(1, n), desc="Chuyển đổi", total=n-1):
        # Nhân với (x - x_{i-1})
        current_poly = np.convolve(current_poly, [1.0, -x_vals[i-1]])
        
        # Cộng newton_coeffs[i] * current_poly vào result
        for j in range(len(current_poly)):
            if j < n:
                result[j] += newton_coeffs[i] * current_poly[j]
    
    return result


def decode_chunked_smart(input_file='encoded.txt', output_file='output.bmp', chunk_size=500):
    """
    Giải mã chunked thông minh - xử lý từng phần nhỏ và kết hợp
    """
    print("🚀 BẮT ĐẦU GIẢI MÃ (Smart Chunked Mode)")
    print("=" * 60)
    
    if not os.path.exists(input_file):
        print(f"❌ File '{input_file}' không tồn tại!")
        sys.exit(1)
    
    file_size_mb = os.path.getsize(input_file) / (1024 * 1024)
    print(f"📁 Kích thước file: {file_size_mb:.2f} MB")
    print(f"⚙️  Chunk size: {chunk_size}")
    
    all_coeffs = []
    chunk_num = 0
    
    with open(input_file, 'r') as f:
        while True:
            x_vals = []
            y_vals = []
            
            # Đọc chunk
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                
                parts = line.strip().split()
                if len(parts) == 2:
                    x_vals.append(int(parts[0]))
                    y_vals.append(int(parts[1]))
            
            if not x_vals:
                break
            
            chunk_num += 1
            print(f"\n📦 Chunk {chunk_num}: {len(x_vals)} điểm")
            
            # Giải chunk bằng Newton
            print(f"   Đang tính toán...")
            start = time.time()
            
            newton_coeffs = newton_interpolation(x_vals, y_vals)
            coeffs = newton_to_standard(x_vals, newton_coeffs)
            
            print(f"   Thời gian: {time.time() - start:.2f}s")
            
            all_coeffs.append(coeffs)
            
            # Giới hạn số chunk để tránh quá nhiều
            if chunk_num >= 20:
                print("\n⚠️  Đã xử lý 20 chunk - dừng để tránh quá tải")
                break
    
    # Kết hợp kết quả
    print(f"\n🔗 Đã xử lý {len(all_coeffs)} chunk")
    
    if len(all_coeffs) == 1:
        final_coeffs = all_coeffs[0]
    else:
        # Lấy chunk có độ dài lớn nhất (thường là chunk đầu tiên)
        max_len = max(len(c) for c in all_coeffs)
        
        # Lấy chunk đầu tiên làm kết quả chính
        final_coeffs = all_coeffs[0]
        
        print(f"   Sử dụng chunk 1 ({len(final_coeffs)} hệ số)")
    
    # Ghi file
    print(f"\n💾 Đang ghi file: {output_file}")
    with open(output_file, 'wb') as f:
        for i in progress_bar(range(len(final_coeffs)), desc="Ghi byte", total=len(final_coeffs)):
            byte_val = int(round(final_coeffs[i])) % 256
            f.write(bytes([byte_val]))
    
    output_size_kb = os.path.getsize(output_file) / 1024
    print(f"✅ Đã ghi {len(final_coeffs)} bytes ({output_size_kb:.2f} KB)")
    
    print("\n🎉 HOÀN THÀNH!")
    
    return final_coeffs


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Giải mã file cực lớn - Phiên bản tối ưu mạnh',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ:
  %(prog)s -i encoded.txt -o output.bmp
  %(prog)s -i huge.txt -o out.bmp --max-degree 2000
  %(prog)s -i encoded.txt -o out.bmp --chunked --chunk-size 500
  
Lưu ý:
  - Phương pháp mặc định: Newton's interpolation (tối ưu nhất)
  - Chunked: Dùng khi file CỰC lớn (> 100MB) hoặc RAM hạn chế
        """
    )
    
    parser.add_argument('-i', '--input', default='encoded.txt',
                       help='File input (mặc định: encoded.txt)')
    parser.add_argument('-o', '--output', default='output.bmp',
                       help='File output (mặc định: output.bmp)')
    parser.add_argument('--max-degree', type=int, default=5000,
                       help='Bậc tối đa của đa thức (mặc định: 5000)')
    parser.add_argument('--chunked', action='store_true',
                       help='Sử dụng chế độ chunked')
    parser.add_argument('--chunk-size', type=int, default=500,
                       help='Kích thước chunk (mặc định: 500)')
    
    args = parser.parse_args()
    
    # Validate
    if args.max_degree < 10:
        print("❌ max_degree phải >= 10")
        sys.exit(1)
    
    if args.chunk_size < 10:
        print("❌ chunk_size phải >= 10")
        sys.exit(1)
    
    # Chạy
    try:
        if args.chunked:
            decode_chunked_smart(args.input, args.output, args.chunk_size)
        else:
            decode_ultra(args.input, args.output, args.max_degree)
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()