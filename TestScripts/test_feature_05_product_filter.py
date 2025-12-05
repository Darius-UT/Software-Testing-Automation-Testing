# -*- coding: utf-8 -*-
import unittest
import csv
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

# --- CẤU HÌNH ĐỂ IMPORT MODULE TỪ THƯ MỤC CHA ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail


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

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.verificationErrors = []

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
        print_header("TEST SUITE: FILTER AUTOMATION")

        # Get the path to the data file relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, '..', 'Data', 'data_filter.csv')

        if not os.path.exists(data_file):
            self.fail(f"Không tìm thấy file dữ liệu tại: {data_file}")

        with open(data_file, 'r', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                test_case_id = row['Case_ID']
                
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Search", row['Data_Search'] if row['Data_Search'] else "(empty)")
                print_info("Price Min", row['Data_PriceMin'] if row['Data_PriceMin'] else "(empty)")
                print_info("Price Max", row['Data_PriceMax'] if row['Data_PriceMax'] else "(empty)")
                print_info("Category", row['Data_Category'] if row['Data_Category'] else "(empty)")

                try:
                    # --- 1. Điều hướng ---
                    driver.get(row['Target_URL'])
                    time.sleep(3)

                    # --- 2. Nhập giá trị filter ---
                    self.set_value(row['Locator_PriceMin'], row['Data_PriceMin'])
                    self.set_value(row['Locator_PriceMax'], row['Data_PriceMax'])

                    # --- 3. Click category nếu có ---
                    if row['Data_Category']:
                        try:
                            driver.find_element(By.PARTIAL_LINK_TEXT, row['Data_Category']).click()
                        except Exception:
                            print_info("Warning", f"Không tìm thấy category: {row['Data_Category']}")

                    # --- 4. Nhập search và submit ---
                    self.set_value(row['Locator_Search'], row['Data_Search'], submit=True)
                    time.sleep(5)

                    # --- 5. Kiểm tra kết quả ---
                    expected_result = row['Expected_Result']
                    if expected_result in driver.page_source:
                        print_pass(f"Tìm thấy kết quả mong đợi: '{expected_result}'")
                    else:
                        error_msg = f"Không tìm thấy kết quả mong đợi: '{expected_result}'"
                        self.verificationErrors.append(f"[{test_case_id}] FAIL: {error_msg}")
                        print_fail(error_msg)

                except AssertionError as e:
                    self.verificationErrors.append(f"[{test_case_id}] FAIL: {str(e)}")
                    print_fail(f"Assertion Error: {str(e)}")
                except Exception as e:
                    self.verificationErrors.append(f"[{test_case_id}] ERROR: {str(e)}")
                    print_fail(f"Runtime Error: {str(e)}")

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
