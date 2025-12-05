# -*- coding: utf-8 -*-
import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# --- CẤU HÌNH IMPORT MODULE UTILITIES ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from Utilities.console_utils import print_header, print_info, print_pass, print_fail
except ImportError:
    def print_header(msg): print(f"\n=== {msg} ===")
    def print_info(lbl, msg): print(f"[INFO] {lbl}: {msg}")
    def print_pass(msg): print(f"[PASS] {msg}")
    def print_fail(msg): print(f"[FAIL] {msg}")

class TestFeature10PurchaseGiftCertificate(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # 1. Khởi tạo Driver
        cls.driver = webdriver.Chrome(executable_path=r'Drivers/chromedriver.exe')
        cls.driver.implicitly_wait(5)
        cls.base_url = "https://ecommerce-playground.lambdatest.io"
        cls.verificationErrors = []

        # 2. Pre-condition: Đăng nhập
        print_header("SETUP CLASS: ĐĂNG NHẬP HỆ THỐNG")
        driver = cls.driver
        try:
            driver.get(f"{cls.base_url}/index.php?route=account/login")
            print_info("Action", "Đang đăng nhập...")
            driver.find_element(By.ID, "input-email").clear()
            driver.find_element(By.ID, "input-email").send_keys("phuc.nguyenl07@hcmut.edu.vn") # Sửa email của bạn
            driver.find_element(By.ID, "input-password").clear()
            driver.find_element(By.ID, "input-password").send_keys("hvK367xXJtdv3G!") # Sửa pass của bạn
            driver.find_element(By.XPATH, "//input[@value='Login']").click()
        except Exception as e:
            print_fail(f"Lỗi Setup: {str(e)}")

    def test_01_purchase_success(self):
        """Test Case Happy Path: Mua Gift Certificate thành công"""
        driver = self.driver
        print_header("TEST SUITE: PURCHASE VOUCHER - SUCCESS CASES")

        csv_path = os.path.join('Data', 'voucher_success.csv')
        if not os.path.exists(csv_path):
            self.fail(f"File not found: {csv_path}")

        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                # Clean keys
                row = {k.strip(): v for k, v in row.items() if k is not None}
                test_case_id = row.get('TestCaseID', 'Unknown')
                
                print(f"\n--------------------------------------------------")
                print_info("Running", f"{test_case_id} - {row.get('Theme', 'No Theme')}")

                try:
                    # 1. Navigate
                    driver.get(f"{self.base_url}/index.php?route=account/voucher")

                    # 2. Fill Form
                    driver.find_element(By.ID, "input-to-name").clear()
                    driver.find_element(By.ID, "input-to-name").send_keys(row['RecipientName'])
                    
                    driver.find_element(By.ID, "input-to-email").clear()
                    driver.find_element(By.ID, "input-to-email").send_keys(row['RecipientEmail'])
                    
                    # Your Name/Email (có thể đã auto-fill, nhưng cứ điền đè lên cho chắc)
                    driver.find_element(By.ID, "input-from-name").clear()
                    driver.find_element(By.ID, "input-from-name").send_keys(row['YourName'])
                    
                    driver.find_element(By.ID, "input-from-email").clear()
                    driver.find_element(By.ID, "input-from-email").send_keys(row['YourEmail'])

                    # 3. Handle Theme (Radio Button)
                    theme = row['Theme']
                    if theme:
                        try:
                            # XPath tìm Label chứa Text theme, rồi click input con của nó
                            driver.find_element(By.XPATH, f"//label[normalize-space()='{theme}']/input").click()
                        except NoSuchElementException:
                            print_fail(f"Không tìm thấy Theme: {theme}")

                    # 4. Message & Amount
                    driver.find_element(By.ID, "input-message").clear()
                    driver.find_element(By.ID, "input-message").send_keys(row['Message'])
                    
                    driver.find_element(By.ID, "input-amount").clear()
                    driver.find_element(By.ID, "input-amount").send_keys(row['Amount'])

                    # 5. Handle Agree Checkbox
                    agree_checkbox = driver.find_element(By.NAME, "agree")
                    is_selected = agree_checkbox.is_selected()
                    should_agree = (row['Agree'] == "Yes")

                    # Logic: Chỉ click nếu trạng thái hiện tại KHÁC trạng thái mong muốn
                    if should_agree and not is_selected:
                        agree_checkbox.click()
                    elif not should_agree and is_selected:
                        agree_checkbox.click()

                    # 6. Submit
                    driver.find_element(By.XPATH, "//input[@value='Continue']").click()
                    time.sleep(1)

                    # 7. Assertions
                    # Check URL
                    expected_url_part = "route=account/voucher/success"
                    if expected_url_part in driver.current_url:
                        print_pass("URL chuyển hướng đúng (Success Page).")
                    else:
                        print_fail(f"URL sai: {driver.current_url}")
                        self.verificationErrors.append(f"[{test_case_id}] Wrong URL")

                    # Check Text
                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    expected_text = row['ExpectedText']
                    if expected_text in body_text:
                        print_pass("Hiển thị thông báo thành công đúng.")
                    else:
                        print_fail(f"Thiếu thông báo: {expected_text}")
                        self.verificationErrors.append(f"[{test_case_id}] Missing success text")

                except Exception as e:
                    print_fail(f"Runtime Error: {str(e)}")
                    self.verificationErrors.append(f"[{test_case_id}] Error: {str(e)}")

    def test_02_purchase_error(self):
        """Test Case Error Path: Kiểm tra Validation và Logic Error"""
        driver = self.driver
        print_header("TEST SUITE: PURCHASE VOUCHER - ERROR CASES")

        csv_path = os.path.join('Data', 'voucher_error.csv')
        if not os.path.exists(csv_path):
            self.fail(f"File not found: {csv_path}")

        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                row = {k.strip(): v for k, v in row.items() if k is not None}
                test_case_id = row.get('TestCaseID', 'Unknown')
                
                print(f"\n--------------------------------------------------")
                print_info("Running", f"{test_case_id}")

                try:
                    # 1. Navigate
                    driver.get(f"{self.base_url}/index.php?route=account/voucher")

                    # 2. Fill Form (Tương tự success nhưng xử lý dữ liệu trống)
                    if row['RecipientName']:
                        driver.find_element(By.ID, "input-to-name").clear()
                        driver.find_element(By.ID, "input-to-name").send_keys(row['RecipientName'])
                    else:
                        driver.find_element(By.ID, "input-to-name").clear() # Xóa trắng để test case empty

                    if row['RecipientEmail']:
                        driver.find_element(By.ID, "input-to-email").clear()
                        driver.find_element(By.ID, "input-to-email").send_keys(row['RecipientEmail'])
                    else:
                        driver.find_element(By.ID, "input-to-email").clear()

                    driver.find_element(By.ID, "input-from-name").clear()
                    driver.find_element(By.ID, "input-from-name").send_keys(row['YourName'])
                    
                    driver.find_element(By.ID, "input-from-email").clear()
                    driver.find_element(By.ID, "input-from-email").send_keys(row['YourEmail'])

                    theme = row['Theme']
                    if theme:
                         try:
                            driver.find_element(By.XPATH, f"//label[normalize-space()='{theme}']/input").click()
                         except: pass # Bỏ qua nếu không tìm thấy theme (để test lỗi)
                    
                    driver.find_element(By.ID, "input-message").send_keys(row['Message'])
                    driver.find_element(By.ID, "input-amount").clear()
                    driver.find_element(By.ID, "input-amount").send_keys(row['Amount'])

                    # Checkbox Logic
                    agree_checkbox = driver.find_element(By.NAME, "agree")
                    should_agree = (row['Agree'] == "Yes")
                    if should_agree and not agree_checkbox.is_selected():
                        agree_checkbox.click()
                    elif not should_agree and agree_checkbox.is_selected():
                        agree_checkbox.click()

                    # 3. Submit
                    driver.find_element(By.XPATH, "//input[@value='Continue']").click()
                    time.sleep(1)

                    # 4. Assertions (Error)
                    expected_url_part = "route=account/voucher" # Vẫn ở trang cũ
                    # Lưu ý: "voucher" nằm trong url voucher/success nên phải check kĩ là KHÔNG có success
                    if "success" not in driver.current_url:
                        print_pass("URL không thay đổi (Đúng).")
                    else:
                        print_fail("Lỗi: Hệ thống chuyển sang trang Success!")
                        self.verificationErrors.append(f"[{test_case_id}] Redirected to Success")

                    # Check Error Message
                    expected_msg = row['ExpectedMessage']
                    page_src = driver.page_source
                    
                    # Tìm lỗi validation (text-danger) hoặc warning (alert-danger)
                    if expected_msg in page_src:
                        print_pass(f"Tìm thấy thông báo lỗi: {expected_msg}")
                    else:
                        print_fail(f"Không tìm thấy lỗi: {expected_msg}")
                        self.verificationErrors.append(f"[{test_case_id}] Missing error message")

                except Exception as e:
                    print_fail(f"Runtime Error: {str(e)}")
                    self.verificationErrors.append(f"[{test_case_id}] Error: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        print_header("TEAR DOWN CLASS")
        cls.driver.quit()
        if cls.verificationErrors:
            print_fail(f"CÓ {len(cls.verificationErrors)} LỖI XẢY RA:")
            for err in cls.verificationErrors:
                print(f"  - {err}")
        else:
            print_pass("Tất cả Test Case hoàn thành xuất sắc!")

if __name__ == "__main__":
    unittest.main()