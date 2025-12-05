# -*- coding: utf-8 -*-
import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
# ActionChains đã được loại bỏ vì không còn cần thiết khi vào link trực tiếp
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ĐỂ IMPORT MODULE TỪ THƯ MỤC CHA ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail

class RegisterTest(unittest.TestCase):

    def setUp(self):
        # Khởi tạo WebDriver
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10) 
        self.driver.maximize_window()
        self.verificationErrors = []

    def test_register(self):
        driver = self.driver
        print_header("TEST SUITE: REGISTER")

        with open("./Data/register_data.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                test_case_id = row["TestCaseID"]
                
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Email", row["email"])
                print_info("Expected Type", row["ExpectedType"])

                try:
                    firstname = row["firstname"]
                    lastname = row["lastname"]
                    email = row["email"]
                    telephone = row["telephone"]
                    password = row["password"]
                    confirmPassword = row["confirmPassword"]
                    privacyCheck = row["PrivacyCheck"]
                    expectedMessage = row["ExpectedMessage"]
                    expectedType = row["ExpectedType"]

                    # Vào thẳng trang Đăng ký 
                    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")
                    time.sleep(1)
                    
                    # Nếu web tự động redirect về trang Account (do chưa logout), thì logout rồi vào lại
                    if "route=account/account" in driver.current_url:
                         driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/logout")
                         time.sleep(1)
                         driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")
                         time.sleep(1)
                    # ĐIỀN FORM 
                    driver.find_element(By.ID, "input-firstname").clear()
                    driver.find_element(By.ID, "input-firstname").send_keys(firstname)
                    
                    driver.find_element(By.ID, "input-lastname").clear()
                    driver.find_element(By.ID, "input-lastname").send_keys(lastname)
                    
                    driver.find_element(By.ID, "input-email").clear()
                    driver.find_element(By.ID, "input-email").send_keys(email)
                    
                    driver.find_element(By.ID, "input-telephone").clear()
                    driver.find_element(By.ID, "input-telephone").send_keys(telephone)
                    
                    driver.find_element(By.ID, "input-password").clear()
                    driver.find_element(By.ID, "input-password").send_keys(password)
                    
                    driver.find_element(By.ID, "input-confirm").clear()
                    driver.find_element(By.ID, "input-confirm").send_keys(confirmPassword)
                    
                    # Checkbox Privacy Policy
                    if privacyCheck.upper() == "TRUE":
                        try:
                            driver.find_element(By.XPATH, "//label[@for='input-agree']").click()
                        except:
                             driver.find_element(By.ID, "input-agree").click()
                    
                    currentURL = driver.current_url
                    
                    # Click nút Continue
                    driver.find_element(By.XPATH, "//input[@value='Continue']").click()
                    time.sleep(2) # Chờ trang load kết quả
                    
                    # --- 4. KIỂM TRA KẾT QUẢ (VALIDATION) ---
                    if expectedType == "success":
                        try:
                            # Tìm thẻ H1 chứa thông báo thành công
                            actual_title = driver.find_element(By.TAG_NAME, "h1").text
                            self.assertEqual(expectedMessage, actual_title)
                            print_pass(f"SUCCESS matched: {expectedMessage}")
                            
                            # Đăng ký thành công thì Logout ngay để dọn dẹp cho vòng lặp sau
                            driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/logout")
                            time.sleep(1)
                            
                        except AssertionError as e:
                            error_msg = f"Assertion Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                            print_fail(error_msg)
                        except Exception as e:
                            error_msg = f"Runtime Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                            print_fail(error_msg)

                    else:  # Trường hợp mong đợi lỗi (Expected Fail)
                        try:
                            # Kiểm tra URL không thay đổi (vẫn ở trang register)
                            if driver.current_url != currentURL:
                                 print_info("Warning", "Trang đã bị chuyển đi, có thể test case sai logic.")

                            # Gom tất cả thông báo lỗi trên màn hình
                            error_msgs = []
                            # Lỗi dạng alert phía trên
                            alert_errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger")
                            for err in alert_errors: error_msgs.append(err.text)
                            
                            # Lỗi text đỏ dưới input
                            text_errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
                            for err in text_errors: error_msgs.append(err.text)
                            
                            all_errors_text = " ".join(error_msgs)
                            
                            print_info("Detected errors", all_errors_text if all_errors_text else "(none)")

                            # Kiểm tra message mong đợi có nằm trong đống lỗi đó không
                            if expectedMessage:
                                # Hỗ trợ check nhiều lỗi ngăn cách bởi dấu chấm phẩy
                                expected_list = [msg.strip() for msg in expectedMessage.split(";")]
                                for msg in expected_list:
                                    self.assertIn(msg, all_errors_text)
                                print_pass(f"ERROR matched: {expectedMessage}")
                            else:
                                print_pass("Registration failed as expected")
                                
                        except AssertionError as e:
                            error_msg = f"Assertion Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                            print_fail(error_msg)
                        except Exception as e:
                            error_msg = f"Runtime Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                            print_fail(error_msg)

                except Exception as e:
                    error_msg = f"Unexpected Error: {str(e)}"
                    self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                    print_fail(error_msg)

    def tearDown(self):
        print_header("TEAR DOWN")
        self.driver.quit()
        
        if self.verificationErrors:
            print_fail(f"CÓ {len(self.verificationErrors)} LỖI XẢY RA TRONG QUÁ TRÌNH CHẠY:")
            for err in self.verificationErrors:
                print(f"  - {err}")
            raise Exception("Test Suite Failed due to verification errors.")
        else:
            print_pass("Tất cả Test Case đã chạy thành công!")

if __name__ == "__main__":
    unittest.main()