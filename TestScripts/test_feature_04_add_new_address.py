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

fields_input = {
    "Locator_FN": "First Name",
    "Locator_LN": "Last Name",
    "Locator_Address1": "Address1",
    "Locator_City": "City",
    "Locator_Postcode": "Postcode"
}

fields_dropdown = {
    "Locator_Country": "Country",
    "Locator_Region": "Region"
}

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail

class TestFeature04AddNewAddress(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_feature03_edit_account(self):
        print_header("TEST SUITE: ADD NEW ADDRESS")
        driver = self.driver
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, '..', 'Data', 'add_new_address.csv')
        with open(data_file, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                test_case_id = row['Testcase ID']
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Input First Name", row['First Name'])
                print_info("Input Last Name", row['Last Name'])
                print_info("Input Address 1", row['Address1'])
                print_info("Input City", row['City'])
                print_info("Input Postcode", row['Postcode'])
                print_info("Select Country", row['Country'])
                print_info("Select Region/State", row['Region'])
                driver.get(row['Target_URL'])
                time.sleep(3)
                driver.find_element(By.XPATH, row['Locator_Username']).clear()
                driver.find_element(By.XPATH, row['Locator_Username']).send_keys(row['Username'])
                driver.find_element(By.XPATH, row['Locator_Password']).clear()
                driver.find_element(By.XPATH, row['Locator_Password']).send_keys(row['Password'])    
                driver.find_element(By.XPATH, row['Locator_LoginBTN']).click()
                time.sleep(5)
                driver.find_element(By.XPATH, row['Locator_AddressBTN']).click()
                time.sleep(5)
                driver.find_element(By.XPATH, row['Locator_NewBTN']).click()
                time.sleep(5)
                for locator_key, field_key in fields_input.items():
                    el = driver.find_element(By.XPATH, row[locator_key])
                    el.clear()
                    el.send_keys(row[field_key])
                # Xử lý dropdown fields
                for locator_key, field_key in fields_dropdown.items():
                    select = Select(driver.find_element(By.XPATH, row[locator_key]))
                    select.select_by_visible_text(row[field_key])
                
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
                    except AssertionError:
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
