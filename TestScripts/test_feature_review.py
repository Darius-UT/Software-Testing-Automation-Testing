# -*- coding: utf-8 -*-
import unittest
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestReview(unittest.TestCase):
    JS_SET_VALUE = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    JS_CHECK_RADIO = """
        arguments[0].checked = true;
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('click', { bubbles: true }));
    """
    LOCATOR_MAP = {
        "id": By.ID, "name": By.NAME, "css": By.CSS_SELECTOR,
        "xpath": By.XPATH, "link_text": By.LINK_TEXT
    }

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def get_element(self, locator_string):
        if not locator_string or "=" not in locator_string:
            return None
        by_type, value = locator_string.split("=", 1)
        by_method = self.LOCATOR_MAP.get(by_type.lower().strip())
        if not by_method:
            return None
        try:
            return self.driver.find_element(by_method, value)
        except Exception:
            return None

    def set_value(self, locator, value, scroll=False):
        elem = self.get_element(locator)
        if not elem or not value:
            return
        if scroll:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
            time.sleep(1)
        self.driver.execute_script(self.JS_SET_VALUE, elem, value)

    def click_element(self, locator):
        elem = self.get_element(locator)
        if elem:
            self.driver.execute_script("arguments[0].click();", elem)

    def set_rating(self, base_locator, rating_value):
        if not rating_value:
            return
        rating_locator = f"{base_locator}[value='{rating_value}']"
        elem = self.get_element(rating_locator)
        if elem:
            self.driver.execute_script(self.JS_CHECK_RADIO, elem)

    def verify_result(self, case_id, expected):
        if expected in self.driver.page_source:
            print("PASSED ✅")
        else:
            print(f"FAILED ❌ (Expected '{expected}' not found)")

    def test_review_automation(self):
        print("\n--- REVIEW AUTOMATION TEST ---")

        with open('data_review.csv', 'r', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                print(f"Running {row['Case_ID']}...", end=" ")
                
                self.driver.get(row['Target_URL'])
                time.sleep(3)
                
                self.click_element(row['Locator_Tab'])
                time.sleep(3)

                self.set_value(row['Locator_Name'], row['Val_Name'], scroll=True)
                self.set_value(row['Locator_Review'], row['Val_Review'])
                self.set_rating(row['Locator_Rating_Base'], row['Val_Rating'])
                
                self.click_element(row['Locator_Btn'])
                time.sleep(5)

                self.verify_result(row['Case_ID'], row['Expected_Result'])

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
