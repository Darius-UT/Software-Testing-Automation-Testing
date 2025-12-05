# -*- coding: utf-8 -*-
import unittest
import os
import sys

# Import bộ màu sắc tiện ích
# Đảm bảo bạn đã có file Utilities/console_utils.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Utilities.console_utils import print_header, print_pass, print_fail, print_info, TextColor

def run_all():
    # 1. Cấu hình Test Loader
    loader = unittest.TestLoader()
    start_dir = 'TestScripts'
    
    if not os.path.exists(start_dir):
        print_fail(f"Không tìm thấy thư mục '{start_dir}'. Hãy đảm bảo bạn đang chạy từ root project.")
        return

    # 2. Tìm kiếm và Gom nhóm
    print_header("BẮT ĐẦU QUÉT VÀ CHẠY TOÀN BỘ TEST SUITE")
    # pattern='test_*.py' để tìm tất cả file bắt đầu bằng test_
    suite = loader.discover(start_dir, pattern='test_*.py')

    # 3. Cấu hình Runner
    runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
    
    # 4. Thực thi
    result = runner.run(suite)

    # 5. Báo cáo Tổng kết
    print_report(result)

def print_report(result):
    """Hàm in báo cáo tổng kết đẹp mắt sau khi chạy xong"""
    print_header("BÁO CÁO TỔNG QUAN (EXECUTION SUMMARY)")

    # Tính toán số lượng
    total_run = result.testsRun
    total_errors = len(result.errors)
    total_failures = len(result.failures)
    total_skipped = len(result.skipped)
    total_passed = total_run - (total_errors + total_failures + total_skipped)

    # In thống kê
    print(f"\n{TextColor.BOLD}THỐNG KÊ:{TextColor.ENDC}")
    print_info("Tổng số Test Case", total_run)
    print(f"  {TextColor.GREEN}✔ PASSED  : {total_passed}{TextColor.ENDC}")
    
    if total_failures > 0 or total_errors > 0:
        print(f"  {TextColor.FAIL}✖ FAILED  : {total_failures}{TextColor.ENDC}")
        print(f"  {TextColor.WARNING}⚠ ERRORS  : {total_errors}{TextColor.ENDC}")
    else:
        print(f"  {TextColor.FAIL}✖ FAILED  : 0{TextColor.ENDC}")
        print(f"  {TextColor.WARNING}⚠ ERRORS  : 0{TextColor.ENDC}")

    if total_skipped > 0:
        print(f"  {TextColor.CYAN}SKIP    : {total_skipped}{TextColor.ENDC}")

    # In danh sách chi tiết các Test Case bị lỗi (nếu có)
    if not result.wasSuccessful():
        print(f"\n{TextColor.BOLD}{TextColor.FAIL}DANH SÁCH LỖI CHI TIẾT:{TextColor.ENDC}")
        print("-" * 60)
        
        all_bad_results = result.failures + result.errors
        
        for test_case, trace_back in all_bad_results:
            # --- SỬA LỖI Ở ĐÂY ---
            # Kiểm tra xem test_case có phải là ErrorHolder (lỗi load file) hay không
            if hasattr(test_case, '_testMethodName'):
                test_name = test_case._testMethodName
                class_name = test_case.__class__.__name__
                identifier = f"{class_name} -> {test_name}"
            else:
                # Nếu là lỗi load file (ImportError, SyntaxError...), lấy mô tả trực tiếp
                identifier = str(test_case)
            
            print(f"{TextColor.FAIL}✖ [FAILED] {identifier}{TextColor.ENDC}")
            
            # Xử lý nội dung lỗi cho gọn
            error_lines = trace_back.strip().split('\n')
            # Lấy dòng cuối cùng thường chứa thông báo lỗi chính
            error_msg = error_lines[-1] if error_lines else "Unknown Error"
            
            print(f"   Lý do: {error_msg}")
            print("-" * 60)
    else:
        print(f"\n{TextColor.GREEN}{TextColor.BOLD}CHÚC MỪNG! TOÀN BỘ HỆ THỐNG HOẠT ĐỘNG ỔN ĐỊNH.{TextColor.ENDC}")

    print_header("KẾT THÚC KIỂM THỬ")

if __name__ == "__main__":
    run_all()