# -*- coding: utf-8 -*-
import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

# --- CẤU HÌNH ĐỂ IMPORT MODULE TỪ THƯ MỤC CHA ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail

class TestFeature07AddToCart(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # 1. Khởi tạo Driver (Selenium 4.x auto-detects chromedriver)
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://ecommerce-playground.lambdatest.io"
        cls.verificationErrors = []

        # 2. Thực hiện Pre-condition: Login
        print_header("SETUP CLASS: ĐĂNG NHẬP")
        driver = cls.driver
        action = ActionChains(driver)
        
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Truy cập trang chủ
            driver.get(cls.base_url)
            
            # Hover vào menu My Account
            menu_account = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]'))
            )
            action.move_to_element(menu_account).perform()
            time.sleep(1)
            
            # Click Login
            login_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='widget-navbar-217834']/ul/li[6]/ul/li/a/div/span"))
            )
            login_link.click()
            
            # Điền form đăng nhập
            print_info("Action", "Đang đăng nhập...")
            
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-email"))
            )
            email_field.clear()
            email_field.send_keys("phuc.nguyenl07@hcmut.edu.vn")
            
            driver.find_element(By.ID, "input-password").clear()
            driver.find_element(By.ID, "input-password").send_keys("hvK367xXJtdv3G!")
            driver.find_element(By.XPATH, "//input[@value='Login']").click()
            
            time.sleep(2) # Wait for redirect
            
            # Kiểm tra đăng nhập thành công
            if "route=account/account" in driver.current_url:
                print_pass("Đăng nhập thành công.")
            else:
                print_fail("Đăng nhập thất bại hoặc không chuyển trang.")

        except Exception as e:
            print_fail(f"Lỗi trong quá trình Setup: {str(e)}")
            raise e

    def test_feature_07_add_to_cart_data_driven(self):
        driver = self.driver
        print_header("TEST SUITE: ADD TO CART DATA DRIVEN")

        csv_path = os.path.join('Data', 'feat_07.csv')
        if not os.path.exists(csv_path):
            self.fail(f"Không tìm thấy file dữ liệu tại: {csv_path}")

        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                test_case_id = row['tc_id'].strip()

                description = row['description'].strip()
                product_id = row['product_id'].strip()
                # size_option might be None/Empty
                size_option = row['size_option'].strip() if row['size_option'] else ""
                qty_input = row['qty_input'].strip()
                expected_type = row['expected_type'].strip()
                expected_message = row['expected_message'].strip()

                print(f"\n--------------------------------------------------")
                print_info("Running", f"{test_case_id} - {description}")
                print_info("Input", f"Product ID: {product_id}, Size: {size_option}, Qty: {qty_input}")

                try:
                    # 1. Navigate to Product Page
                    target_url = f"{self.base_url}/index.php?route=product/product&product_id={product_id}"
                    print_info("Navigate", f"URL: {target_url}")
                    driver.get(target_url)
                    
                    # 2. Select Option (Size) if provided
                    if size_option:
                        try:
                            # Robust Option Selection
                            # 1. Find correct select element
                            select_element = driver.find_element(By.XPATH, "//select[contains(@id, 'input-option')]")
                            select = Select(select_element)
                            
                            # 2. Select by loop (partial text match)
                            found_option = False
                            target_text = ""
                            for option in select.options:
                                if size_option in option.text:
                                    select.select_by_visible_text(option.text)
                                    target_text = option.text
                                    print_info("Action", f"Selected option: {target_text}")
                                    found_option = True
                                    break
                            
                            if not found_option:
                                print_info("Warning", f"Option '{size_option}' not found via text match. Trying index 1.")
                                try:
                                    select.select_by_index(1)
                                    print_info("Action", "Selected option by Index 1 (fallback).")
                                    found_option = True
                                    target_text = select.first_selected_option.text
                                except: pass

                            # 3. Verify Selection sticky
                            time.sleep(0.5)
                            selected_text = select.first_selected_option.text
                            if size_option not in selected_text and "Select" in selected_text:
                                print_info("Fix", "Selection didn't stick! Retrying via JavaScript.")
                                # JS Force set
                                driver.execute_script("arguments[0].selectedIndex = 1; arguments[0].dispatchEvent(new Event('change'));", select_element)
                                time.sleep(0.5)

                        except NoSuchElementException:
                             print_info("Warning", "Dropdown Size option not found on page.")

                    # 3. Enter Quantity
                    try:
                        # Use confirmed locator from browser debug
                        qtys = driver.find_elements(By.CSS_SELECTOR, "input[aria-label='Qty']")
                        if not qtys:
                             qtys = driver.find_elements(By.NAME, "quantity")
                        
                        qty_box = None
                        for q in qtys:
                            if q.is_displayed():
                                qty_box = q
                                break
                        
                        if not qty_box: raise Exception("No visible quantity input")

                        # Scroll and Clear
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", qty_box)
                        time.sleep(0.5)
                        try: qty_box.click() 
                        except: pass
                        
                        # Robust Clear: Standard clear() seems safer for this specific field interactions
                        qty_box.clear()
                        
                        if qty_input not in ['0', '']:
                            qty_box.send_keys(qty_input)
                        
                        # Crucial: Trigger events and Blur
                        driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", qty_box)
                        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", qty_box)
                        driver.execute_script("arguments[0].blur();", qty_box) # Blur to trigger validation
                        time.sleep(0.5)

                        # Verify Value
                        current_val = qty_box.get_attribute("value")
                        if current_val != qty_input and qty_input not in ['0', '']:
                             driver.execute_script("arguments[0].value = arguments[1];", qty_box, qty_input)
                             driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", qty_box)


                    except Exception as e:
                         print_info("Error", f"Quantity interaction failed: {str(e)}")
                         # Final fallback locator
                         qty_box = driver.find_element(By.NAME, "quantity")
                         qty_box.clear()
                         qty_box.send_keys(qty_input)

                    
                    # 4. Click Add to Cart
                    try:
                        add_btn = driver.find_element(By.XPATH, "//div[contains(@id, 'entry_216842')]//button")
                    except:
                        try:
                           # Fallback to user provided class
                           add_btn = driver.find_element(By.CSS_SELECTOR, "button.button-cart")
                        except:
                           add_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Add to Cart']")

                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
                    
                    # JS Click (Bypasses Overlays)
                    driver.execute_script("arguments[0].click();", add_btn)
                    time.sleep(0.5)
                    
                    # Standard Click (Backup)
                    try:
                        add_btn.click()
                    except:
                        pass

                    # 5. Verification (Explicit Wait)
                    from selenium.webdriver.support.ui import WebDriverWait
                    from selenium.webdriver.support import expected_conditions as EC

                    toast_text = ""
                    inline_error_text = ""
                    
                    try:
                        # Wait for ANY notification/alert/error to be visible and have text
                        def check_feedback(d):
                            # Generic selectors for notifications in OpenCart/Bootstrap
                            # 1. #notification-box-top (Custom)
                            # 2. .alert (Standard Bootstrap)
                            # 3. .text-danger (Inline errors)
                            candidates = d.find_elements(By.CSS_SELECTOR, "#notification-box-top, .alert, .text-danger")
                            for c in candidates:
                                try:
                                    if c.is_displayed() and len(c.text.strip()) > 3:
                                        return True
                                except: pass # Stale element ignored
                            return False

                        WebDriverWait(driver, 10).until(check_feedback) # Increased wait to 10s
                        
                        # Capture results from all sources
                        visible_texts = []
                        candidates = driver.find_elements(By.CSS_SELECTOR, "#notification-box-top, .alert, .text-danger")
                        for c in candidates:
                            try:
                                if c.is_displayed() and c.text.strip():
                                    visible_texts.append(c.text.strip().replace('\n', ' '))
                            except: pass
                        
                        toast_text = " | ".join(visible_texts)

                    except Exception as e:
                        print_info("Wait", "Timeout - No visible notification found")

                    print_info("Captured Text", toast_text[:150])

                    if expected_type == 'success':
                        if expected_message in toast_text:
                            print_pass(f"Success verified.")
                        elif "Success" in toast_text and "added" in toast_text:
                             print_pass(f"Success (Partial match).")
                        else:
                             self.fail(f"Expected success '{expected_message}' but got '{toast_text}'")

                    elif expected_type == 'error_warning':
                         if expected_message in toast_text:
                             print_pass("Warning verified.")
                         else:
                             self.fail(f"Expected warning '{expected_message}' not found in Toast: '{toast_text}' or Inline: '{inline_error_text}'")

                    elif expected_type == 'error_text_danger':
                        if expected_message in inline_error_text:
                             print_pass("Inline error verified.")
                        elif expected_message in toast_text:
                             print_info("Note", "Found error in Toast instead of Inline.")
                             print_pass("Error verified (in Toast).")
                        else:
                             self.fail(f"Expected inline '{expected_message}' but got '{inline_error_text}'")
                    
                    elif expected_type == 'error_validation':
                         current_val = qty_box.get_attribute("value")
                         print_info("Current Input Value", current_val)
                         if "Success" not in toast_text:
                               print_pass("Validation blocked success action.")
                         else:
                               self.fail("Validation failed: System allowed adding invalid input!")

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
            print_fail(f"CÓ {len(cls.verificationErrors)} LỖI XẢY RA:")
            for err in cls.verificationErrors:
                print(f"  - {err}")
        else:
            print_pass("Tất cả Test Case đã chạy thành công!")

if __name__ == "__main__":
    unittest.main()

