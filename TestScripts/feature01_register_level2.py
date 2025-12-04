# -*- coding: utf-8 -*-
import unittest
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


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

        with open("./Data/register_data.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                print("\n=== RUNNING:", row["TestCaseID"], "===")

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

                # Nếu bị redirect sang trang Account thì logout rồi vào lại, dùng URL trong locator
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
                        print(f"✓ SUCCESS matched: {expectedMessage}")

                        driver.get(self.loc["logout_url"][1])
                        time.sleep(1)

                    except Exception as e:
                        print(f"✗ FAIL: {e}")
                        self.verificationErrors.append(f"{row['TestCaseID']} Failed: {str(e)}")

                else:
                    try:
                        if driver.current_url != currentURL:
                            print("  -> Cảnh báo: Trang đã bị chuyển đi, có thể test case sai logic.")

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
                        print(f"  -> Errors found on screen: {all_errors_text}")

                        # Kiểm tra ExpectedMessage trong errors (hỗ trợ nhiều message bằng ';')
                        if expectedMessage:
                            expected_list = [msg.strip() for msg in expectedMessage.split(";")]
                            for msg in expected_list:
                                self.assertIn(msg, all_errors_text)
                            print(f"✓ ERROR matched: {expectedMessage}")
                        else:
                            print("✓ Registration failed as expected")

                    except Exception as e:
                        print(f"✗ FAIL: {e}")
                        self.verificationErrors.append(f"{row['TestCaseID']} Failed: {str(e)}")

    def tearDown(self):
        print("\n=== TEST FINISHED ===")
        self.assertEqual([], self.verificationErrors)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
