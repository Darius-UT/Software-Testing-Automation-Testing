import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail

class AppDynamicsJob(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.verificationErrors = []

    # LOGIN FUNCTION
    def login(self, driver, email, password):
        driver.get("https://ecommerce-playground.lambdatest.io/")

        my_account = driver.find_element(By.LINK_TEXT, "My account")
        ActionChains(driver).move_to_element(my_account).perform()
        time.sleep(1)

        # Click Login
        driver.find_element(By.LINK_TEXT, "Login").click()

        # Input email & password
        driver.find_element(By.ID, "input-email").clear()
        driver.find_element(By.ID, "input-email").send_keys(email)

        driver.find_element(By.ID, "input-password").clear()
        driver.find_element(By.ID, "input-password").send_keys(password)

        driver.find_element(By.XPATH, "//input[@value='Login']").click()

    def open_change_password(self, driver):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'route=account/password')]"))
        ).click()

    def test_app_dynamics_job(self):
        driver = self.driver
        print_header("TEST SUITE: CHANGE PASSWORD")

        with open("./Data/change_password_data.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                test_case_id = row["TestcaseID"]
                
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Email", row["email"])
                print_info("Expected Type", row["ExpectedType"])

                try:
                    email = row["email"]
                    password = row["password"]
                    changePassword = row["changePassword"]
                    confirmPassword = row["confirmPassword"]
                    expectedType = row["ExpectedType"]
                    expectedMessage = row["ExpectedMessage"]

                    # 1. LOGIN
                    self.login(driver, email, password)
                    time.sleep(1)

                    # 2. Change Password
                    self.open_change_password(driver)

                    driver.find_element(By.ID, "input-password").clear()
                    driver.find_element(By.ID, "input-password").send_keys(changePassword)

                    driver.find_element(By.ID, "input-confirm").clear()
                    driver.find_element(By.ID, "input-confirm").send_keys(confirmPassword)

                    driver.find_element(By.XPATH, "//input[@value='Continue']").click()
                    time.sleep(1.5)

                    # 3. VALIDATION
                    if expectedType == "success":
                        try:
                            msg = driver.find_element(By.CSS_SELECTOR, ".alert-success").text
                            self.assertIn(expectedMessage, msg)
                            print_pass(f"SUCCESS matched: {expectedMessage}")
                        except AssertionError as e:
                            error_msg = f"Assertion Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                            print_fail(error_msg)
                        except Exception as e:
                            error_msg = f"Runtime Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                            print_fail(error_msg)

                    else:  # ERROR CASE
                        try:
                            error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
                            all_errors = " ".join([e.text for e in error_elements])

                            print_info("Detected errors", all_errors if all_errors else "(none)")

                            expected_list = [msg.strip() for msg in expectedMessage.split(";")]

                            for msg in expected_list:
                                self.assertIn(msg, all_errors)

                            print_pass(f"ERROR matched: {expectedMessage}")

                        except AssertionError as e:
                            error_msg = f"Assertion Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                            print_fail(error_msg)
                        except Exception as e:
                            error_msg = f"Runtime Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                            print_fail(error_msg)

                    # 4. LOGOUT
                    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/logout")
                    time.sleep(1)

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
