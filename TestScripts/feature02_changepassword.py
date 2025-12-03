# -*- coding: utf-8 -*-
import unittest
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class AppDynamicsJob(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.implicitly_wait(10)
        self.verificationErrors = []

    # LOGIN FUNCTION
    def login(self, driver, email, password):
        driver.get("https://ecommerce-playground.lambdatest.io/")

        # Hover My account
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

    # NAVIGATE TO CHANGE PASSWORD PAGE
    def open_change_password(self, driver):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'route=account/password')]"))
        ).click()

    def test_app_dynamics_job(self):
        driver = self.driver

        with open("./Data/change_password_data.csv", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                print("\n=== RUNNING:", row["TestcaseID"], "===")

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
                        print("✓ SUCCESS matched:", expectedMessage)
                    except Exception as e:
                        print("✗ FAIL:", e)
                        self.verificationErrors.append(str(e))

                else:  # ERROR CASE
                    try:
                        # Collect all validation errors
                        error_elements = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
                        all_errors = " ".join([e.text for e in error_elements])

                        print("Detected errors:", all_errors)

                        # Support multiple error messages separated by ";"
                        expected_list = [msg.strip() for msg in expectedMessage.split(";")]

                        for msg in expected_list:
                            self.assertIn(msg, all_errors)

                        print("✓ ERROR matched:", expectedMessage)

                    except Exception as e:
                        print("✗ FAIL:", e)
                        self.verificationErrors.append(str(e))

                # 4. LOGOUT
                driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/logout")
                time.sleep(1)

    def tearDown(self):
        print("\n=== TEST FINISHED ===")
        self.assertEqual([], self.verificationErrors)
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
