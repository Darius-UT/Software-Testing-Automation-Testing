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

    def test_review_automation(self):
        driver = self.driver
        print_header("TEST SUITE: REVIEW AUTOMATION")

        # Get the path to the data file relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_file = os.path.join(script_dir, '..', 'Data', 'data_review.csv')

        if not os.path.exists(data_file):
            self.fail(f"Không tìm thấy file dữ liệu tại: {data_file}")

        with open(data_file, 'r', encoding='utf-8') as file:
            for row in csv.DictReader(file):
                test_case_id = row['Case_ID']
                
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Name", row['Val_Name'] if row['Val_Name'] else "(empty)")
                print_info("Review", (row['Val_Review'][:50] + "...") if row['Val_Review'] and len(row['Val_Review']) > 50 else (row['Val_Review'] if row['Val_Review'] else "(empty)"))
                print_info("Rating", row['Val_Rating'] if row['Val_Rating'] else "(empty)")

                try:
                    # --- 1. Điều hướng ---
                    driver.get(row['Target_URL'])
                    time.sleep(3)

                    # --- 2. Click tab Reviews ---
                    self.click_element(row['Locator_Tab'])
                    time.sleep(3)

                    # --- 3. Nhập thông tin review ---
                    self.set_value(row['Locator_Name'], row['Val_Name'], scroll=True)
                    self.set_value(row['Locator_Review'], row['Val_Review'])
                    self.set_rating(row['Locator_Rating_Base'], row['Val_Rating'])

                    # --- 4. Click nút Submit ---
                    self.click_element(row['Locator_Btn'])
                    time.sleep(5)

                    # --- 5. Kiểm tra kết quả ---
                    expected_result = row['Expected_Result']
                    if expected_result in driver.page_source:
                        print_pass(f"Tìm thấy kết quả mong đợi: '{expected_result[:50]}...'")
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
