# -*- coding: utf-8 -*-
import csv
import os
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

class TestFeature03EditAccount(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_feature03_edit_account(self):
        driver = self.driver
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, '..', 'Data', 'edit_account.csv')
        with open(data_file, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Running {row['Testcase ID']}...", end=" ")
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
                if row['Type'] == "Text":
                    element = driver.find_element(By.XPATH, row['Locator_Message'])
                    actual_text = element.text
                    assert actual_text == row['Expected Message'], f"Lỗi: Mong đợi {row['Expected Message']} nhưng nhận được '{actual_text}'"
                elif row['Type'] == "Validation":
                    js_script = f'return document.getElementById("{row['Locator_Message']}").validationMessage.includes("{row['Expected Message']}");'
                    is_valid = driver.execute_script(js_script)
    
                    assert is_valid is True, f"Lỗi: Validation message không chứa '{row['Expected Message']}'"
                driver.find_element(By.XPATH, row['Locator_LogoutBTN']).click()
                time.sleep(5)
                print("Pass")            
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
