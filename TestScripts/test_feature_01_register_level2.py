import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ĐỂ IMPORT MODULE TỪ THƯ MỤC CHA ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail


# ---------------------------------------------------------
# HELPER — LOAD LOCATORS FROM CSV (Level 2)
# ---------------------------------------------------------
def load_locators(file_path):
    locators = {}
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            locators[row["Name"]] = (row["Type"], row["Value"])
    return locators


class RegisterLevel2(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Load locator file 
        self.loc = load_locators("./Data/register_locator.csv")
        self.verificationErrors = []

    def find(self, loc_name):
        loc_type, loc_value = self.loc[loc_name]

        if loc_type == "id":
            return self.driver.find_element(By.ID, loc_value)
        if loc_type == "css":
            return self.driver.find_element(By.CSS_SELECTOR, loc_value)
        if loc_type == "xpath":
            return self.driver.find_element(By.XPATH, loc_value)
        if loc_type == "link_text":
            return self.driver.find_element(By.LINK_TEXT, loc_value)
        return None

    # -----------------------------------------------------
    # MAIN TEST (Level 2, data-driven)
    # -----------------------------------------------------
    def test_register(self):
        driver = self.driver
        print_header("TEST SUITE: REGISTER (LEVEL 2)")

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

                    # 1. Vào trang Register từ locator data
                    register_url = self.loc["register_url"][1]
                    driver.get(register_url)
                    time.sleep(1)

                    # Nếu bị redirect sang trang Account thì logout rồi vào lại
                    if "route=account/account" in driver.current_url:
                        driver.get(self.loc["logout_url"][1])
                        time.sleep(1)
                        driver.get(register_url)
                        time.sleep(1)

                    # 2. Điền form 
                    self.find("firstname_input").clear()
                    self.find("firstname_input").send_keys(firstname)

                    self.find("lastname_input").clear()
                    self.find("lastname_input").send_keys(lastname)

                    self.find("email_input").clear()
                    self.find("email_input").send_keys(email)

                    self.find("telephone_input").clear()
                    self.find("telephone_input").send_keys(telephone)

                    self.find("password_input").clear()
                    self.find("password_input").send_keys(password)

                    self.find("confirm_password_input").clear()
                    self.find("confirm_password_input").send_keys(confirmPassword)

                    # 3. Checkbox Privacy Policy 
                    if privacyCheck.upper() == "TRUE":
                        try:
                            self.find("privacy_label").click()
                        except Exception:
                            self.find("privacy_checkbox").click()

                    currentURL = driver.current_url

                    # 4. Click Continue
                    self.find("continue_button").click()
                    time.sleep(2)

                    # 5. VALIDATION 
                    if expectedType == "success":
                        try:
                            actual_title = self.find("success_title").text
                            self.assertEqual(expectedMessage, actual_title)
                            print_pass(f"SUCCESS matched: {expectedMessage}")

                            driver.get(self.loc["logout_url"][1])
                            time.sleep(1)

                        except AssertionError as e:
                            error_msg = f"Assertion Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                            print_fail(error_msg)
                        except Exception as e:
                            error_msg = f"Runtime Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                            print_fail(error_msg)

                    else:
                        try:
                            if driver.current_url != currentURL:
                                print_info("Warning", "Trang đã bị chuyển đi, có thể test case sai logic.")

                            error_msgs = []

                            try:
                                alert_errors = driver.find_elements(By.CSS_SELECTOR, self.loc["alert_danger"][1])
                                for err in alert_errors:
                                    error_msgs.append(err.text)
                            except Exception:
                                pass

                            # Text đỏ dưới input
                            try:
                                text_errors = driver.find_elements(By.CSS_SELECTOR, self.loc["danger_text"][1])
                                for err in text_errors:
                                    error_msgs.append(err.text)
                            except Exception:
                                pass

                            all_errors_text = " ".join(error_msgs)
                            print_info("Detected errors", all_errors_text if all_errors_text else "(none)")

                            if expectedMessage:
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
