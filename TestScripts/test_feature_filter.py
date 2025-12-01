# -*- coding: utf-8 -*-
import unittest
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestFilter(unittest.TestCase):
    JS_SET_VALUE = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """
    JS_SET_AND_SUBMIT = """
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        arguments[0].dispatchEvent(new KeyboardEvent('keypress', { key: 'Enter', keyCode: 13, bubbles: true }));
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

    def set_value(self, locator, value, submit=False):
        elem = self.get_element(locator)
        if elem and value:
            js = self.JS_SET_AND_SUBMIT if submit else self.JS_SET_VALUE
            self.driver.execute_script(js, elem, value)

    def test_filter_automation(self):
        driver = self.driver
        print("\n--- FILTER AUTOMATION TEST ---")

        with open('data_filter.csv', 'r', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                print(f"Running {row['Case_ID']}...", end=" ")
                
                driver.get(row['Target_URL'])
                time.sleep(3)
                
                self.set_value(row['Locator_PriceMin'], row['Data_PriceMin'])
                self.set_value(row['Locator_PriceMax'], row['Data_PriceMax'])

                if row['Data_Category']:
                    try:
                        driver.find_element(By.PARTIAL_LINK_TEXT, row['Data_Category']).click()
                    except Exception:
                        pass

                self.set_value(row['Locator_Search'], row['Data_Search'], submit=True)
                time.sleep(5)

                if row['Expected_Result'] in driver.page_source:
                    print("PASSED ✅")
                else:
                    print(f"FAILED ❌ (Expected '{row['Expected_Result']}' not found)")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
