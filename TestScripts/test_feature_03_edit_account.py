# -*- coding: utf-8 -*-
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail

class TestFeature03EditAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(30)
        cls.base_url = "https://www.google.com/"
        cls.verificationErrors = []
        cls.accept_next_alert = True
    
    def test_feature03_edit_account(self):
        print_header("TEST SUITE: EDIT ACCOUNT")
        driver = self.driver
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, '..', 'Data', 'edit_account.csv')
        with open(data_file, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                test_case_id = row['Testcase ID']
                print(f"\n--------------------------------------------------")
                print_info("Running", row['Testcase ID'])
                print_info("Input First Name", row['First Name'])
                print_info("Input Last Name", row['Last Name'])
                print_info("Input E-MAIL", row['E-MAIL'])
                print_info("Input Telephone", row['Telephone'])
                driver.get(row['Target_URL'])
                time.sleep(3)
                driver.find_element(By.XPATH, row['Locator_Username']).clear()
                driver.find_element(By.XPATH, row['Locator_Username']).send_keys(row['Username'])
                driver.find_element(By.XPATH, row['Locator_Password']).clear()
                driver.find_element(By.XPATH, row['Locator_Password']).send_keys(row['Password'])    
                driver.find_element(By.XPATH, row['Locator_LoginBTN']).click()
                time.sleep(5)
                driver.find_element(By.XPATH, row['Locator_EditBTN']).click()
                time.sleep(5)
                driver.find_element(By.XPATH, row['Locator_FN']).clear()
                driver.find_element(By.XPATH, row['Locator_FN']).send_keys(row['First Name'])
                driver.find_element(By.XPATH, row['Locator_LN']).clear()
                driver.find_element(By.XPATH, row['Locator_LN']).send_keys(row['Last Name'])
                driver.find_element(By.XPATH, row['Locator_Email']).clear()
                driver.find_element(By.XPATH, row['Locator_Email']).send_keys(row['E-MAIL'])
                driver.find_element(By.XPATH, row['Locator_Telephone']).clear()
                driver.find_element(By.XPATH, row['Locator_Telephone']).send_keys(row['Telephone'])
                form = driver.find_element(By.XPATH, row['Locator_ContinueBTN'])  # chỉnh theo form của bạn
                form.submit()

                time.sleep(3)

                expected_msg = row['Expected Message']

                if row['Type'] == "Text":
                    try:
                        element = driver.find_element(By.XPATH, row['Locator_Message'])
                        actual_text = element.text
                        self.assertEqual(actual_text, expected_msg)
                        print_pass(f"Hiển thị đúng thông báo: '{actual_text}'")
                    except AssertionError as e:
                        msg = f"Sai nội dung thông báo! Mong đợi: '{expected_msg}', Thực tế: '{actual_text}'"
                        print_fail(msg)
                        self.verificationErrors.append(f"[{test_case_id}] {msg}")

                elif row['Type'] == "Validation":
                    locator_id = row['Locator_Message']
                    js_script = f'return document.getElementById("{locator_id}").validationMessage;'
                    actual_validation = driver.execute_script(js_script)
                    
                    if expected_msg in actual_validation:
                            print_pass(f"Validation message chuẩn: '{actual_validation}'")
                    else:
                            msg = f"Validation sai! Mong đợi chứa '{expected_msg}', Thực tế: '{actual_validation}'"
                            print_fail(msg)
                            self.verificationErrors.append(f"[{test_case_id}] {msg}")
                driver.find_element(By.XPATH, row['Locator_LogoutBTN']).click()
                time.sleep(5)
                print("Pass")            
    
    @classmethod
    def tearDownClass(cls):
        print_header("TEAR DOWN CLASS")
        cls.driver.quit()
        
        if cls.verificationErrors:
            print_fail(f"CÓ {len(cls.verificationErrors)} LỖI XẢY RA TRONG QUÁ TRÌNH CHẠY:")
            for err in cls.verificationErrors:
                print(f"  - {err}")
            raise Exception("Test Suite Failed due to verification errors.")
        else:
            print_pass("Tất cả Test Case đã chạy thành công!")

if __name__ == "__main__":
    unittest.main()
