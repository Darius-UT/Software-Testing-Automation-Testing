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

# --- CẤU HÌNH ĐỂ IMPORT MODULE TỪ THƯ MỤC CHA ---
# Giúp Python tìm thấy folder Utilities khi chạy file này
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Utilities.console_utils import print_header, print_info, print_pass, print_fail

class TestFeature09ManageShoppingCartQuantity(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # 1. Khởi tạo Driver
        # Lưu ý: Cập nhật đường dẫn driver chính xác trên máy bạn
        cls.driver = webdriver.Chrome(executable_path=r'Drivers/chromedriver.exe')
        cls.driver.implicitly_wait(10)
        cls.base_url = "https://ecommerce-playground.lambdatest.io"
        cls.verificationErrors = []

        # 2. Thực hiện Pre-condition: Login và Add Product
        print_header("SETUP CLASS: ĐĂNG NHẬP VÀ THÊM SẢN PHẨM")
        driver = cls.driver
        action = ActionChains(driver)
        
        try:
            # Truy cập trang chủ
            driver.get(cls.base_url)
            
            # Hover vào menu My Account (dùng XPath ngắn gọn hơn nếu được)
            menu_account = driver.find_element(By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]')
            action.move_to_element(menu_account).perform()
            time.sleep(1) # Chờ menu xổ xuống
            
            # Click Login
            driver.find_element(By.XPATH, "//div[@id='widget-navbar-217834']/ul/li[6]/ul/li/a/div/span").click()
            
            # Điền form đăng nhập
            # (Nên đưa thông tin này vào file config hoặc biến môi trường để bảo mật hơn)
            print_info("Action", "Đang đăng nhập...")
            driver.find_element(By.ID, "input-email").clear()
            driver.find_element(By.ID, "input-email").send_keys("phuc.nguyenl07@hcmut.edu.vn")
            driver.find_element(By.ID, "input-password").clear()
            driver.find_element(By.ID, "input-password").send_keys("hvK367xXJtdv3G!")
            driver.find_element(By.XPATH, "//input[@value='Login']").click()
            
            # Kiểm tra đăng nhập thành công (chuyển hướng đến trang Account)
            if "route=account/account" in driver.current_url:
                print_pass("Đăng nhập thành công.")
            else:
                print_fail("Đăng nhập thất bại hoặc không chuyển trang.")

            # Thêm sản phẩm vào giỏ (Product ID 64 - Palm Treo Pro)
            print_info("Action", "Đang thêm sản phẩm Palm Treo Pro vào giỏ...")
            driver.get(f"{cls.base_url}/index.php?route=product/product&product_id=64")
            
            # Nhập số lượng 5
            driver.find_element(By.XPATH, "//div[@id='entry_216841']/div/input").clear()
            driver.find_element(By.XPATH, "//div[@id='entry_216841']/div/input").send_keys("5")
            driver.find_element(By.XPATH, "//div[@id='entry_216842']/button").click()
            
            time.sleep(2) # Chờ thông báo success
            print_pass("Đã thêm sản phẩm vào giỏ hàng.")

        except Exception as e:
            print_fail(f"Lỗi trong quá trình Setup: {str(e)}")
            raise e

    # # Test case cho trường hợp Happy-path
    def test_01_feature_09_update_success(self):
        driver = self.driver
        print_header("TEST SUITE: UPDATE CART SUCCESS")

        # Đường dẫn file CSV
        csv_path = os.path.join('Data', 'cart_update_success.csv')

        if not os.path.exists(csv_path):
            self.fail(f"Không tìm thấy file dữ liệu tại: {csv_path}")

        # Đọc file CSV
        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                test_case_id = row['TestCaseID']
                product_name = row['ProductName'] # Quan trọng: Dùng tên sản phẩm để định vị
                
                # In thông tin Test Case đang chạy
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Product", product_name)
                print_info("Input Qty", row['InputQuantity'])

                try:
                    # --- 1. Điều hướng ---
                    website_url = row['WebsiteUrl']
                    if "http" in website_url:
                        driver.get(website_url)
                    else:
                        driver.get(self.base_url + website_url)

                    # --- 2. Xác định Locator Động (Dynamic XPath) ---
                    # Tìm dòng chứa tên sản phẩm
                    row_xpath = f"//tr[td//a[contains(text(), '{product_name}')]]"
                    
                    # Tìm ô Input nằm trong dòng đó (quan trọng: dùng contains @name 'quantity')
                    # Cách này không cần quan tâm số ID là bao nhiêu (quantity[123] hay quantity[456] đều chạy được)
                    input_xpath = f"{row_xpath}//input[contains(@name, 'quantity')]"
                    
                    # Tìm nút Update nằm trong dòng đó (dùng icon refresh)
                    update_btn_xpath = f"{row_xpath}//button[i[contains(@class, 'fa-sync-alt')]]"

                    # --- 3. Thao tác ---
                    # Nhập liệu (Dùng XPath động vừa tạo)
                    qty_input = driver.find_element(By.XPATH, input_xpath)
                    qty_input.click()
                    qty_input.clear()
                    qty_input.send_keys(row['InputQuantity'])

                    # Click Update
                    driver.find_element(By.XPATH, update_btn_xpath).click()
                    
                    time.sleep(2) # Chờ load

                    # --- 4. Kiểm tra kết quả (Verification) ---
                    
                    # A. Kiểm tra thông báo
                    actual_message = driver.find_element(By.XPATH, "//*[@id='checkout-cart']/div[1]").text
                    self.assertIn(row['ExpectedMessage'], actual_message)
                    print_pass("Thông báo thành công hiển thị đúng.")

                    # B. Kiểm tra giá trị ô Input (Tìm lại element để tránh Stale)
                    actual_quantity = driver.find_element(By.XPATH, input_xpath).get_attribute("value")
                    self.assertEqual(row['ExpectedQuantity'], actual_quantity)
                    print_pass(f"Số lượng cập nhật đúng: {actual_quantity}")

                    # C. Kiểm tra tính tiền
                    # Lấy Unit Price (Cột 5)
                    unit_price_str = driver.find_element(By.XPATH, f"{row_xpath}//td[5]").text
                    unit_price = float(unit_price_str.replace('$', '').replace(',', ''))

                    # Tính toán Expected Total
                    calc_expected_total = unit_price * float(row['ExpectedQuantity'])

                    # Lấy Actual Total (Cột 6)
                    actual_total_str = driver.find_element(By.XPATH, f"{row_xpath}//td[6]").text
                    actual_total = float(actual_total_str.replace('$', '').replace(',', ''))

                    # So sánh
                    if abs(actual_total - calc_expected_total) > 0.01:
                        error_msg = f"Sai giá tiền! Thực tế: {actual_total}, Tính toán: {calc_expected_total}"
                        self.verificationErrors.append(f"[{test_case_id}] {error_msg}")
                        print_fail(error_msg)
                    else:
                        print_pass(f"Tính tiền đúng: ${actual_total}")

                except AssertionError as e:
                    self.verificationErrors.append(f"[{test_case_id}] FAIL: {str(e)}")
                    print_fail(f"Assertion Error: {str(e)}")
                except Exception as e:
                    self.verificationErrors.append(f"[{test_case_id}] ERROR: {str(e)}")
                    print_fail(f"Runtime Error: {str(e)}")

    # Test case cho trường hợp Error-path
    def test_02_feature_09_update_error(self):
        driver = self.driver
        print_header("TEST SUITE: UPDATE CART ERROR")

        # 1. Đường dẫn file CSV Error
        csv_path = os.path.join('Data', 'cart_update_error.csv')

        if not os.path.exists(csv_path):
            self.fail(f"Không tìm thấy file dữ liệu tại: {csv_path}")

        # 2. Đọc file CSV
        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                test_case_id = row['TestCaseID']
                
                # In thông tin format đẹp
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Input Invalid Qty", row['InputQuantity'])

                try:
                    # --- Thao tác trên trình duyệt (Dựa trên code gốc) ---
                    
                    # 1. Mở URL (Xử lý biến ${WebsiteUrl})
                    # Lưu ý: CSV cần có cột 'WebsiteUrl' hoặc bạn gán cứng nếu muốn
                    website_url = row.get('WebsiteUrl', '/index.php?route=checkout/cart')
                    if "http" in website_url:
                        driver.get(website_url)
                    else:
                        driver.get(self.base_url + website_url)

                    # 2. Click & Clear & Type vào ô Input
                    # Xây dựng XPath động dựa trên ${ProductName}
                    product_name = row['ProductName']
                    input_quantity = row['InputQuantity']
                    
                    # XPath tìm ô input theo tên sản phẩm
                    input_xpath = f"//tr[td//a[contains(text(), '{product_name}')]]//input[contains(@name, 'quantity')]"
                    
                    driver.find_element(By.XPATH, input_xpath).click()
                    driver.find_element(By.XPATH, input_xpath).clear()
                    driver.find_element(By.XPATH, input_xpath).send_keys(input_quantity)

                    # 3. Click nút Update
                    # Xây dựng XPath động dựa trên ${DataOriginalTitle}
                    # Lưu ý: CSV cần có cột 'DataOriginalTitle' (VD: Update)
                    data_title = row.get('DataOriginalTitle', 'Update') 
                    button_xpath = f"//tr[td//a[contains(text(), '{product_name}')]]//button[@title='{data_title}']"
                    
                    driver.find_element(By.XPATH, button_xpath).click()
                    
                    time.sleep(2) # Chờ phản hồi

                    # --- Kiểm tra kết quả (Verification) ---
                    
                    # 4. Verify Error Message (Dựa trên code gốc: //*[@id="checkout-cart"]/div[2])
                    # Lưu ý: Code gốc trỏ vào div[2], nghĩa là mong đợi thông báo lỗi nằm ở vị trí thứ 2
                    try:
                        error_msg_element = driver.find_element(By.XPATH, "//*[@id='checkout-cart']/div[2]")
                        actual_error_msg = error_msg_element.text
                        expected_message = row['ExpectedMessage']
                        
                        self.assertIn(expected_message, actual_error_msg)
                        print_pass(f"Thông báo lỗi hiển thị đúng: {expected_message[:30]}...")
                    except NoSuchElementException: # type: ignore
                        raise AssertionError("Không tìm thấy thông báo lỗi tại vị trí div[2] như kịch bản!")

                    # 5. Verify Text Not Present (Không hiển thị thông báo thành công)
                    # Dùng regex hoặc assertNotIn
                    not_expected_msg = "Success: You have modified your shopping cart!"
                    page_source = driver.find_element(By.TAG_NAME, "body").text
                    
                    self.assertNotIn(not_expected_msg, page_source)
                    print_pass("Không hiển thị thông báo Success.")

                except AssertionError as e:
                    self.verificationErrors.append(f"[{test_case_id}] FAIL: {str(e)}")
                    print_fail(f"Assertion Error: {str(e)}")
                except Exception as e:
                    self.verificationErrors.append(f"[{test_case_id}] ERROR: {str(e)}")
                    print_fail(f"Runtime Error: {str(e)}")
                    self.verificationErrors.append(f"[{test_case_id}] ERROR: {str(e)}")
                    print_fail(f"Runtime Error: {str(e)}")

    # Test case cho trường hợp Remove-path (Direct và In-direct)
    def test_03_feature_09_remove_item(self):
        driver = self.driver
        print_header("TEST SUITE: REMOVE ITEM (DESTRUCTIVE CASES)")

        # Đường dẫn file CSV
        csv_path = os.path.join('Data', 'cart_remove.csv')
        if not os.path.exists(csv_path):
            self.fail(f"Không tìm thấy file dữ liệu tại: {csv_path}")

        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                test_case_id = row['TestCaseID']
                product_name = row['ProductName']
                
                print(f"\n--------------------------------------------------")
                print_info("Running", test_case_id)
                print_info("Action Type", row['ActionType'])

                try:
                    # --- BƯỚC PHỤ: HỒI SINH SẢN PHẨM ---
                    # Logic: Nếu sản phẩm không có trong giỏ -> Thêm lại
                    driver.get(self.base_url + "/index.php?route=checkout/cart")
                    
                    # Tìm dòng chứa tên sản phẩm
                    row_xpath = f"//tr[td//a[contains(text(), '{product_name}')]]"
                    products_in_cart = driver.find_elements(By.XPATH, row_xpath)
                    
                    if len(products_in_cart) == 0:
                        print_info("Auto-Fix", "Giỏ hàng đang trống/thiếu SP, đang thêm lại...")
                        driver.get(f"{self.base_url}/index.php?route=product/product&product_id=64")
                        # Nút Add to Cart ở trang chi tiết
                        driver.find_element(By.XPATH, "//div[@id='entry_216842']/button").click()
                        time.sleep(2) # Chờ thêm xong
                        driver.get(self.base_url + "/index.php?route=checkout/cart")
                    
                    # --- BẮT ĐẦU TEST CHÍNH ---
                    
                    if row['ActionType'] == 'Update':
                        # 1. Nhập liệu (Tìm input dựa vào row_xpath đã xác định ở trên)
                        input_xpath = f"{row_xpath}//input[contains(@name, 'quantity')]"
                        
                        driver.find_element(By.XPATH, input_xpath).click()
                        driver.find_element(By.XPATH, input_xpath).clear()
                        driver.find_element(By.XPATH, input_xpath).send_keys(row['InputQuantity'])
                        
                        # 2. Bấm Update (Sửa locator: Tìm nút có chứa icon refresh 'fa-sync-alt')
                        # Cách này an toàn hơn dùng @title
                        update_btn_xpath = f"{row_xpath}//button[i[contains(@class, 'fa-sync-alt')]]"
                        driver.find_element(By.XPATH, update_btn_xpath).click()
                        
                    elif row['ActionType'] == 'RemoveBtn':
                        # Case bấm nút Xóa trực tiếp
                        # Sửa locator: Tìm nút có chứa icon xóa 'fa-times-circle'
                        remove_btn_xpath = f"{row_xpath}//button[i[contains(@class, 'fa-times-circle')]]"
                        driver.find_element(By.XPATH, remove_btn_xpath).click()

                    time.sleep(2) # Chờ load

                    # --- VERIFY KẾT QUẢ ---
                    
                    # 1. Kiểm tra thông báo Success
                    try:
                        actual_msg = driver.find_element(By.XPATH, "//*[@id='checkout-cart']/div[1]").text
                        self.assertIn(row['ExpectedMessage'], actual_msg)
                        print_pass("Hiển thị thông báo xóa thành công.")
                    except NoSuchElementException:
                         # Đôi khi xóa xong nó hiện text ở content chứ không phải alert
                         print_info("Note", "Không thấy alert xanh, kiểm tra danh sách sản phẩm...")

                    # 2. Kiểm tra Sản phẩm BIẾN MẤT (Quan trọng nhất)
                    # Tìm lại dòng chứa sản phẩm
                    products_remaining = driver.find_elements(By.XPATH, f"//tr[td//a[contains(text(), '{product_name}')]]")
                    
                    if len(products_remaining) == 0:
                        print_pass(f"Sản phẩm '{product_name}' đã biến mất khỏi giỏ hàng.")
                    else:
                        # Kiểm tra kỹ hơn: Có thể sản phẩm vẫn còn nhưng layout khác?
                        # Hoặc check xem có dòng "Your shopping cart is empty!" không
                        empty_msg = driver.find_elements(By.XPATH, "//div[@id='content']/p[contains(text(), 'Your shopping cart is empty!')]")
                        if len(empty_msg) > 0:
                             print_pass("Giỏ hàng đã trống (Sản phẩm đã bị xóa).")
                        else:
                             raise AssertionError("Sản phẩm vẫn còn tồn tại trong giỏ sau khi xóa!")

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