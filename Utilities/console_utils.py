# -*- coding: utf-8 -*-

class TextColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Các hàm in ấn dùng chung ---

def print_header(text):
    print(f"\n{TextColor.HEADER}{TextColor.BOLD}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{TextColor.ENDC}")

def print_pass(message):
    print(f"  [{TextColor.GREEN}PASSED{TextColor.ENDC}] {message}")

def print_fail(message):
    print(f"  [{TextColor.FAIL}FAILED{TextColor.ENDC}] {message}")

def print_info(label, value):
    print(f"  {TextColor.CYAN}➤ {label:<15}{TextColor.ENDC}: {value}")