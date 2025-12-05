# -*- coding: utf-8 -*-
import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ĐỂ IMPORT MODULE TỪ THƯ MỤC CHA ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail


# ---------------------------------------------------------
# HELPER — LOAD LOCATORS FROM CSV
# ---------------------------------------------------------
def load_locators(file_path):
    locators = {}
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            locators[row["Name"]] = (row["Type"], row["Value"])
    return locators


# ---------------------------------------------------------
# MAIN TEST CLASS
# ---------------------------------------------------------
class ChangePasswordLevel2(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)

        # Load locator file from Data folder
        self.loc = load_locators("./Data/changepassword_locator.csv")
        self.verificationErrors = []


    # -----------------------------------------------------
    # FUNCTION: Find element by dynamic locator
    # -----------------------------------------------------
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
    # LOGIN FUNCTION (Level 2)
    # -----------------------------------------------------
    def login(self, email, password):
        driver = self.driver
        driver.get(self.loc["base_url"][1])

        # Hover
        my_account = self.find("menu_my_account")
        ActionChains(driver).move_to_element(my_account).perform()
        # Wait for the dropdown to open and the Login link to be clickable
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, self.loc["login_link"][1]))
            ).click()
        except Exception:
            # Fallback: navigate directly to login page if link not found/clickable
            driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

        # Ensure the login form is present before entering credentials
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, self.loc["email_input"][1]))
        )

        # Enter credentials
        self.find("email_input").clear()
        self.find("email_input").send_keys(email)

        self.find("password_input").clear()
        self.find("password_input").send_keys(password)

        self.find("login_button").click()


    # -----------------------------------------------------
    # OPEN CHANGE PASSWORD
    # -----------------------------------------------------
    def open_change_pw(self):
        loc_type, loc_value = self.loc["change_password_link"]
        by_map = {
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "link_text": By.LINK_TEXT,
        }
        by = by_map.get(loc_type, By.XPATH)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by, loc_value))
        )
        self.find("change_password_link").click()


    # -----------------------------------------------------
    # MAIN TEST
    # -----------------------------------------------------
    def test_change_password(self):
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
                    # Step 1: login
                    self.login(row["email"], row["password"])
                    time.sleep(1)

                    # Step 2: open change password page
                    self.open_change_pw()

                    # Step 3: enter new password
                    self.find("new_password_input").clear()
                    self.find("new_password_input").send_keys(row["changePassword"])

                    self.find("confirm_password_input").clear()
                    self.find("confirm_password_input").send_keys(row["confirmPassword"])

                    self.find("continue_button").click()
                    time.sleep(1.2)

                    # Step 4: VALIDATION
                    if row["ExpectedType"] == "success":
                        try:
                            msg = self.find("success_alert").text
                            self.assertIn(row["ExpectedMessage"], msg)
                            print_pass(f"SUCCESS: {row['ExpectedMessage']}")
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
                            errors = ""
                            elements = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
                            errors = " ".join([e.text for e in elements])

                            print_info("Detected errors", errors if errors else "(none)")

                            for msg in row["ExpectedMessage"].split(";"):
                                self.assertIn(msg.strip(), errors)

                            print_pass(f"ERROR matched: {row['ExpectedMessage']}")

                        except AssertionError as e:
                            error_msg = f"Assertion Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                            print_fail(error_msg)
                        except Exception as e:
                            error_msg = f"Runtime Error: {str(e)}"
                            self.verificationErrors.append(f"[{test_case_id}] ERROR: {error_msg}")
                            print_fail(error_msg)

                    # Step 5: logout
                    driver.get(self.loc["logout_url"][1])
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
