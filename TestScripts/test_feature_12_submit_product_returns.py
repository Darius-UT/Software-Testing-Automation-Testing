# -*- coding: utf-8 -*-
import unittest
import time
import csv
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

# --- CẤU HÌNH IMPORT MODULE UTILITIES ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from Utilities.console_utils import print_header, print_info, print_pass, print_fail
except ImportError:
    # Fallback nếu không tìm thấy file utils (để code không lỗi ngay lập tức khi copy chạy thử)
    def print_header(msg): print(f"\n=== {msg} ===")
    def print_info(lbl, msg): print(f"[INFO] {lbl}: {msg}")
    def print_pass(msg): print(f"[PASS] {msg}")
    def print_fail(msg): print(f"[FAIL] {msg}")

class TestFeature12SubmitProductReturns(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # 1. Khởi tạo Driver
        # Cập nhật đường dẫn driver tương ứng trên máy của bạn
        cls.driver = webdriver.Chrome(executable_path=r'Drivers/chromedriver.exe')
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://ecommerce-playground.lambdatest.io"
        cls.verificationErrors = []

        # 2. Pre-condition: Đăng nhập (Thường cần đăng nhập để trả hàng hoặc lấy thông tin order)
        print_header("SETUP CLASS: ĐĂNG NHẬP HỆ THỐNG")
        driver = cls.driver
        
        try:
            driver.get(f"{cls.base_url}/index.php?route=account/login")
            
            # Điền form đăng nhập (Thông tin mẫu, bạn hãy sửa lại account thật của bạn)
            print_info("Action", "Đang đăng nhập...")
            driver.find_element(By.ID, "input-email").clear()
            driver.find_element(By.ID, "input-email").send_keys("phuc.nguyenl07@hcmut.edu.vn") # Thay bằng email thật
            driver.find_element(By.ID, "input-password").clear()
            driver.find_element(By.ID, "input-password").send_keys("hvK367xXJtdv3G!") # Thay bằng pass thật
            driver.find_element(By.XPATH, "//input[@value='Login']").click()
            
            # Kiểm tra đăng nhập
            if "route=account/account" in driver.current_url:
                print_pass("Đăng nhập thành công.")
            else:
                print_info("Warning", "Có thể đăng nhập không thành công hoặc không chuyển trang, tiếp tục thử test case.")

        except Exception as e:
            print_fail(f"Lỗi trong quá trình Setup: {str(e)}")
            # Không raise e ở đây để cho phép chạy thử test case kể cả khi login lỗi (nếu form return public)

    # def test_tc012_01_return_submit_success(self):
    #     driver = self.driver
    #     print_header("TEST SUITE: SUBMIT PRODUCT RETURN SUCCESS")

    #     # Đường dẫn file CSV
    #     csv_path = os.path.join('Data', 'return_submit_success.csv')

    #     if not os.path.exists(csv_path):
    #         self.fail(f"Không tìm thấy file dữ liệu tại: {csv_path}")

    #     # Đọc file CSV
    #     with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
    #         reader = csv.DictReader(csvfile)
            
    #         for row in reader:
    #             test_case_id = row['TestCaseID']
                
    #             print(f"\n--------------------------------------------------")
    #             print_info("Running", test_case_id)
    #             print_info("Order ID", row['OrderID'])
    #             print_info("Product", row['ProductName'])

    #             try:
    #                 # --- 1. Điều hướng đến trang Return ---
    #                 driver.get(f"{self.base_url}/index.php?route=account/return/add")

    #                 # --- 2. Điền thông tin cá nhân (Personal Details) ---
    #                 # Lưu ý: Nếu đã login, các trường này có thể tự điền, ta dùng clear() trước cho chắc
    #                 driver.find_element(By.ID, "input-firstname").clear()
    #                 driver.find_element(By.ID, "input-firstname").send_keys(row['FirstName'])
                    
    #                 driver.find_element(By.ID, "input-lastname").clear()
    #                 driver.find_element(By.ID, "input-lastname").send_keys(row['LastName'])
                    
    #                 driver.find_element(By.ID, "input-email").clear()
    #                 driver.find_element(By.ID, "input-email").send_keys(row['Email'])
                    
    #                 driver.find_element(By.ID, "input-telephone").clear()
    #                 driver.find_element(By.ID, "input-telephone").send_keys(row['Telephone'])

    #                 # --- 3. Điền thông tin đơn hàng (Order Information) ---
    #                 driver.find_element(By.ID, "input-order-id").clear()
    #                 driver.find_element(By.ID, "input-order-id").send_keys(row['OrderID'])
                    
    #                 # Xử lý Date Picker: Thay vì click popup, ta gửi text trực tiếp (Format YYYY-MM-DD)
    #                 driver.find_element(By.ID, "input-date-ordered").clear()
    #                 driver.find_element(By.ID, "input-date-ordered").send_keys(row['DateOrdered'])
    #                 # Tắt popup lịch nếu nó hiện ra che khuất phần tử khác (nhấn phím TAB hoặc click ra ngoài)
    #                 driver.find_element(By.ID, "input-date-ordered").click() 

    #                 # --- 4. Điền thông tin sản phẩm (Product Information) ---
    #                 driver.find_element(By.ID, "input-product").clear()
    #                 driver.find_element(By.ID, "input-product").send_keys(row['ProductName'])
                    
    #                 driver.find_element(By.ID, "input-model").clear()
    #                 driver.find_element(By.ID, "input-model").send_keys(row['ProductCode'])
                    
    #                 driver.find_element(By.ID, "input-quantity").clear()
    #                 driver.find_element(By.ID, "input-quantity").send_keys(row['Quantity'])

    #                 # --- 5. Chọn Reason và Opened (Radio Buttons động) ---
    #                 # Reason for Return
    #                 reason_val = row['Reason'] # Ví dụ: "Dead On Arrival" hoặc "Order Error"
    #                 # XPath tìm label chứa text Reason, sau đó tìm input radio đi kèm
    #                 reason_xpath = f"//label[normalize-space()='{reason_val}']/input"
    #                 driver.find_element(By.XPATH, reason_xpath).click()

    #                 # Product is opened
    #                 opened_val = row['Opened'] # "Yes" or "No"
    #                 opened_xpath = f"//label[normalize-space()='{opened_val}']/input[@name='opened']"
    #                 driver.find_element(By.XPATH, opened_xpath).click()

    #                 # Faulty or other details
    #                 driver.find_element(By.ID, "input-comment").clear()
    #                 driver.find_element(By.ID, "input-comment").send_keys(row['Description'])

    #                 # --- 6. Submit ---
    #                 driver.find_element(By.XPATH, "//input[@value='Submit']").click()
                    
    #                 time.sleep(2) # Chờ server xử lý

    #                 # --- 7. Verification ---
                    
    #                 # Check URL
    #                 current_url = driver.current_url
    #                 if "route=account/return/success" in current_url:
    #                     print_pass("URL chuyển hướng đúng (Success Page).")
    #                 else:
    #                     print_fail(f"URL sai: {current_url}")
    #                     self.verificationErrors.append(f"[{test_case_id}] Wrong URL redirect")

    #                 # Check Success Message Text
    #                 try:
    #                     # Dựa vào code cũ: //*[@id="content"]/p[2]
    #                     success_msg = driver.find_element(By.XPATH, "//div[@id='content']/p[contains(text(), 'Thank you for submitting')]").text
    #                     expected_text = "Thank you for submitting your return request"
                        
    #                     if expected_text in success_msg:
    #                         print_pass("Hiển thị thông báo thành công đúng nội dung.")
    #                     else:
    #                         print_fail(f"Nội dung thông báo sai: {success_msg}")
    #                         self.verificationErrors.append(f"[{test_case_id}] Wrong success message")
                            
    #                 except NoSuchElementException:
    #                     print_fail("Không tìm thấy thông báo thành công trên trang.")
    #                     self.verificationErrors.append(f"[{test_case_id}] Success message element not found")

    #                 # Check Continue Button exists
    #                 try:
    #                     driver.find_element(By.XPATH, "//a[text()='Continue']")
    #                     print_pass("Nút Continue hiển thị.")
    #                 except NoSuchElementException:
    #                     print_fail("Nút Continue không hiển thị.")

    #             except AssertionError as e:
    #                 self.verificationErrors.append(f"[{test_case_id}] FAIL: {str(e)}")
    #                 print_fail(f"Assertion Error: {str(e)}")
    #             except Exception as e:
    #                 self.verificationErrors.append(f"[{test_case_id}] ERROR: {str(e)}")
    #                 print_fail(f"Runtime Error: {str(e)}")

    # def test_tc012_02_return_submit_error(self):
    #     driver = self.driver
    #     print_header("TEST SUITE: SUBMIT PRODUCT RETURN ERROR VALIDATION")

    #     # Đường dẫn file CSV
    #     csv_path = os.path.join('Data', 'return_submit_error.csv')

    #     if not os.path.exists(csv_path):
    #         self.fail(f"Không tìm thấy file dữ liệu tại: {csv_path}")

    #     # Đọc file CSV
    #     with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
    #         reader = csv.DictReader(csvfile)
            
    #         for row in reader:
    #             test_case_id = row['TestCaseID']
                
    #             print(f"\n--------------------------------------------------")
    #             print_info("Running", test_case_id)
    #             print_info("Description", row['Description'])
    #             print_info("Expected Error", row['ExpectedMessage'])

    #             try:
    #                 # --- 1. Điều hướng đến trang Return ---
    #                 driver.get(f"{self.base_url}/index.php?route=account/return/add")
    #                 time.sleep(1)

    #                 # --- 2. Điền thông tin cá nhân (Personal Details) ---
    #                 driver.find_element(By.ID, "input-firstname").clear()
    #                 if row['FirstName']:
    #                     driver.find_element(By.ID, "input-firstname").send_keys(row['FirstName'])
                    
    #                 driver.find_element(By.ID, "input-lastname").clear()
    #                 if row['LastName']:
    #                     driver.find_element(By.ID, "input-lastname").send_keys(row['LastName'])
                    
    #                 driver.find_element(By.ID, "input-email").clear()
    #                 if row['Email']:
    #                     driver.find_element(By.ID, "input-email").send_keys(row['Email'])
                    
    #                 driver.find_element(By.ID, "input-telephone").clear()
    #                 if row['Telephone']:
    #                     driver.find_element(By.ID, "input-telephone").send_keys(row['Telephone'])

    #                 # --- 3. Điền thông tin đơn hàng (Order Information) ---
    #                 driver.find_element(By.ID, "input-order-id").clear()
    #                 if row['OrderID']:
    #                     driver.find_element(By.ID, "input-order-id").send_keys(row['OrderID'])
                    
    #                 # Xử lý Date Picker
    #                 driver.find_element(By.ID, "input-date-ordered").clear()
    #                 if row['DateOrdered']:
    #                     driver.find_element(By.ID, "input-date-ordered").send_keys(row['DateOrdered'])
    #                 driver.find_element(By.ID, "input-date-ordered").click()

    #                 # --- 4. Điền thông tin sản phẩm (Product Information) ---
    #                 driver.find_element(By.ID, "input-product").clear()
    #                 if row['ProductName']:
    #                     driver.find_element(By.ID, "input-product").send_keys(row['ProductName'])
                    
    #                 driver.find_element(By.ID, "input-model").clear()
    #                 if row['ProductCode']:
    #                     driver.find_element(By.ID, "input-model").send_keys(row['ProductCode'])
                    
    #                 driver.find_element(By.ID, "input-quantity").clear()
    #                 if row['Quantity']:
    #                     driver.find_element(By.ID, "input-quantity").send_keys(row['Quantity'])

    #                 # --- 5. Chọn Reason và Opened (Radio Buttons động) ---
    #                 # Reason for Return - chỉ chọn nếu có giá trị
    #                 if row['Reason']:
    #                     reason_val = row['Reason']
    #                     reason_xpath = f"//label[normalize-space()='{reason_val}']/input"
    #                     try:
    #                         driver.find_element(By.XPATH, reason_xpath).click()
    #                     except NoSuchElementException:
    #                         print_info("Warning", f"Không tìm thấy reason: {reason_val}")

    #                 # Product is opened - chỉ chọn nếu có giá trị
    #                 if row['Opened']:
    #                     opened_val = row['Opened']
    #                     opened_xpath = f"//label[normalize-space()='{opened_val}']/input[@name='opened']"
    #                     try:
    #                         driver.find_element(By.XPATH, opened_xpath).click()
    #                     except NoSuchElementException:
    #                         print_info("Warning", f"Không tìm thấy opened option: {opened_val}")

    #                 # --- 6. Submit ---
    #                 driver.find_element(By.XPATH, "//input[@value='Submit']").click()
                    
    #                 time.sleep(2) # Chờ server xử lý

    #                 # --- 7. Verification ---
                    
    #                 # Check URL - phải vẫn ở trang return/add (không chuyển sang success)
    #                 current_url = driver.current_url
    #                 if "route=account/return/add" in current_url:
    #                     print_pass("URL giữ nguyên trang return/add (lỗi không submit được).")
    #                 else:
    #                     print_fail(f"URL đã chuyển hướng (không mong muốn): {current_url}")
    #                     self.verificationErrors.append(f"[{test_case_id}] URL should stay on return/add page")

    #                 # Check Error Message xuất hiện
    #                 expected_message = row['ExpectedMessage']
    #                 try:
    #                     # Tìm thông báo lỗi - thường ở trong div.alert hoặc div.text-danger
    #                     page_text = driver.find_element(By.CSS_SELECTOR, "body").text
                        
    #                     if expected_message in page_text:
    #                         print_pass(f"Hiển thị thông báo lỗi đúng: '{expected_message}'")
    #                     else:
    #                         print_fail(f"Không tìm thấy thông báo lỗi: '{expected_message}'")
    #                         print_info("Page Text", page_text[:500])  # In 500 ký tự đầu để debug
    #                         self.verificationErrors.append(f"[{test_case_id}] Expected error message not found")
                            
    #                 except NoSuchElementException:
    #                     print_fail("Không tìm thấy body element để kiểm tra message.")
    #                     self.verificationErrors.append(f"[{test_case_id}] Cannot verify error message")

    #                 # Verify form data vẫn giữ nguyên
    #                 try:
    #                     actual_firstname = driver.find_element(By.ID, "input-firstname").get_attribute("value")
    #                     if actual_firstname == row['FirstName']:
    #                         print_pass("FirstName giữ nguyên trong form.")
    #                     else:
    #                         print_info("Info", f"FirstName thay đổi: {row['FirstName']} -> {actual_firstname}")
    #                 except:
    #                     pass

    #             except AssertionError as e:
    #                 self.verificationErrors.append(f"[{test_case_id}] FAIL: {str(e)}")
    #                 print_fail(f"Assertion Error: {str(e)}")
    #             except Exception as e:
    #                 self.verificationErrors.append(f"[{test_case_id}] ERROR: {str(e)}")
    #                 print_fail(f"Runtime Error: {str(e)}")

    def test_tc012_03_history_autofill_flow(self):
        driver = self.driver
        print_header("TEST SUITE: HISTORY AUTO-FILL & SUBMIT")

        csv_path = os.path.join('Data', 'return_history_autofill.csv')
        if not os.path.exists(csv_path):
            self.fail(f"Không tìm thấy file: {csv_path}")

        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            
            for row in reader:
                row = {k.strip(): v for k, v in row.items() if k is not None}
                test_case_id = row.get('TestCaseID', 'TC-Unknown')
                order_id = row['OrderID']
                target_product = row['TargetProductName']

                print(f"\n--------------------------------------------------")
                print_info("Running", f"{test_case_id} - Order #{order_id}")

                try:
                    # --- BƯỚC 1: ĐIỀU HƯỚNG ---
                    driver.get(f"{self.base_url}/index.php?route=account/order")
                    
                    # --- BƯỚC 2: TÌM ĐƠN HÀNG & VIEW (DIRECT CLICK) ---
                    try:
                        time.sleep(2) # Chờ bảng load
                        
                        # --- XPATH CHIẾN LƯỢC ---
                        # Logic: Tìm thẻ <tr> mà bên trong nó có thẻ <td> chứa text Order ID
                        # Sau đó, ngay trong thẻ <tr> đó, tìm thẻ <a> có class='btn-info' (nút View)
                        view_btn_xpath = f"//tr[td[contains(text(), '{order_id}')]]//a[contains(@class, 'btn-info')]"
                        
                        view_btn = driver.find_element(By.XPATH, view_btn_xpath)
                        
                        # --- DIRECT JS CLICK (QUAN TRỌNG) ---
                        # Lệnh này ép trình duyệt click thẳng vào element, bỏ qua hover/tooltip
                        driver.execute_script("arguments[0].click();", view_btn)
                        
                        print_pass(f"Đã bấm View đơn hàng #{order_id}")
                        time.sleep(1) # Chờ trang chi tiết load

                    except NoSuchElementException:
                        print_fail(f"Không tìm thấy đơn hàng #{order_id} (hoặc XPath sai).")
                        continue 

                    # --- BƯỚC 3: TÌM SẢN PHẨM & CLICK RETURN (DIRECT CLICK) ---
                    try:
                        # Logic tương tự: Tìm dòng chứa tên SP -> Tìm nút Return (nút màu đỏ btn-danger)
                        # Link nút return thường chứa: route=account/return/add
                        return_btn_xpath = f"//tr[td[contains(text(), '{target_product}')]]//a[contains(@href, 'return/add')]"
                        
                        return_btn = driver.find_element(By.XPATH, return_btn_xpath)
                        
                        # Click trực tiếp bằng JS luôn cho chắc ăn
                        driver.execute_script("arguments[0].click();", return_btn)
                        
                        print_pass(f"Đã bấm Return cho sản phẩm: {target_product}")
                        time.sleep(1)
                        
                    except NoSuchElementException:
                        print_fail(f"Không tìm thấy sản phẩm '{target_product}' trong đơn hàng.")
                        continue

                    # --- BƯỚC 4: VERIFY AUTO-FILL ---
                    act_order_id = driver.find_element(By.ID, "input-order-id").get_attribute("value")
                    act_product = driver.find_element(By.ID, "input-product").get_attribute("value")
                    
                    if str(order_id) == act_order_id:
                        print_pass(f"Auto-fill Order ID đúng: {act_order_id}")
                    else:
                        print_fail(f"Auto-fill sai Order ID. Kì vọng: {order_id}, Thực tế: {act_order_id}")
                        self.verificationErrors.append(f"[{test_case_id}] Order ID mismatch")

                    if target_product == act_product:
                        print_pass(f"Auto-fill Product Name đúng: {act_product}")
                    else:
                        print_fail(f"Auto-fill sai Product Name. Thực tế: {act_product}")
                        self.verificationErrors.append(f"[{test_case_id}] Product Name mismatch")

                    # --- BƯỚC 5: SUBMIT ---
                    if row['Reason']:
                        # Dùng JS Click cho radio button luôn để tránh bị label che
                        reason_elem = driver.find_element(By.XPATH, f"//label[normalize-space()='{row['Reason']}']/input")
                        driver.execute_script("arguments[0].click();", reason_elem)
                    
                    if row['Opened']:
                        opened_elem = driver.find_element(By.XPATH, f"//label[normalize-space()='{row['Opened']}']/input[@name='opened']")
                        driver.execute_script("arguments[0].click();", opened_elem)

                    submit_btn = driver.find_element(By.XPATH, "//input[@value='Submit']")
                    driver.execute_script("arguments[0].click();", submit_btn)
                    time.sleep(1)

                    # --- BƯỚC 6: VERIFY SUCCESS ---
                    if "route=account/return/success" in driver.current_url:
                        print_pass("Gửi yêu cầu thành công.")
                    else:
                        print_fail(f"Lỗi Submit. URL: {driver.current_url}")
                        self.verificationErrors.append(f"[{test_case_id}] Submit failed")

                except Exception as e:
                    print_fail(f"Runtime Error: {str(e)}")
                    self.verificationErrors.append(f"[{test_case_id}] Exception: {str(e)}")
    
    @classmethod
    def tearDownClass(cls):
        print_header("TEAR DOWN CLASS")
        cls.driver.quit()
        if cls.verificationErrors:
            print_fail(f"CÓ {len(cls.verificationErrors)} LỖI XẢY RA:")
            for err in cls.verificationErrors:
                print(f"  - {err}")
            # raise Exception("Test Suite Failed") # Uncomment nếu muốn fail build
        else:
            print_pass("Tất cả Test Case hoàn thành xuất sắc!")

if __name__ == "__main__":
    unittest.main()