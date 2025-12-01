# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, re

class TestFeature09CartManage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r'Drivers/chromedriver.exe')
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True


        driver = self.driver
        action = ActionChains(driver)
        
        driver.get("https://ecommerce-playground.lambdatest.io")
        element_to_hover = driver.find_element_by_xpath('//*[@id="widget-navbar-217834"]/ul/li[6]')
        action.move_to_element(element_to_hover).perform()
        
        driver.find_element_by_xpath("//div[@id='widget-navbar-217834']/ul/li[6]/ul/li/a/div/span").click()
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        driver.find_element_by_id("input-email").clear()
        driver.find_element_by_id("input-email").send_keys("phuc.nguyenl07@hcmut.edu.vn")
        driver.find_element_by_id("input-password").clear()
        driver.find_element_by_id("input-password").send_keys("hvK367xXJtdv3G!")
        driver.find_element_by_xpath("//input[@value='Login']").click()
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/account")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=64")

        driver.find_element_by_xpath("//div[@id='entry_216841']/div/input").clear()
        driver.find_element_by_xpath("//div[@id='entry_216841']/div/input").send_keys("10")
        driver.find_element_by_xpath("//div[@id='entry_216842']/button").click()
        
    
    def test_sample(self):
        driver = self.driver

        # Mở file CSV
        with open('./Data/update_cart_data.csv', mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Bắt đầu vòng lặp qua từng dòng
            for row in reader:
                print("Test ở Quantity = ", row["Quantity"], "\n")
                # Di chuyển driver.get vào trong vòng lặp để mỗi lần test lại load lại trang (hoặc giữ nguyên nếu muốn flow liên tục)
                driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
                time.sleep(1) # Chờ trang load nhẹ
        
                driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
                driver.find_element_by_xpath("//tr[td//a[contains(text(), 'Palm Treo Pro')]]//input[contains(@name, 'quantity')]").click()
                driver.find_element_by_xpath("//tr[td//a[contains(text(), 'Palm Treo Pro')]]//input[contains(@name, 'quantity')]").clear()
                driver.find_element_by_xpath("//tr[td//a[contains(text(), 'Palm Treo Pro')]]//input[contains(@name, 'quantity')]").send_keys(row["Quantity"])
                driver.find_element_by_xpath("//div[@id='content']/form/div/table/tbody/tr/td[4]/div/div/button/i").click()
                driver.find_element_by_xpath("//div[@id='checkout-cart']/div").click()
                
                
                if row['ExpectedType'] == "Success" :
                    try: self.assertIn(row["ExpectedMessage"], driver.find_element_by_xpath("//*[@id=\"checkout-cart\"]/div[1]").text)
                    except AssertionError as e: self.verificationErrors.append(str(e))
                    try: self.assertEqual(row["Quantity"], driver.find_element_by_xpath("//div[@id='content']/form/div/table/tbody/tr/td[4]/div/input").get_attribute("value"))
                    except AssertionError as e: self.verificationErrors.append(str(e))
                elif row['ExpectedType'] == "Remove" :
                    try: self.assertIn(row["ExpectedMessage"], driver.find_element_by_xpath("//*[@id=\"checkout-cart\"]/div[1]").text)
                    except AssertionError as e: self.verificationErrors.append(str(e))
                    try: self.assertFalse(self.is_element_present(By.XPATH, "//*[@id=\"content\"]/form/div/table/tbody/tr[1]/td[2]/a"))
                    except AssertionError as e: self.verificationErrors.append(str(e))
                else: 
                    try: self.assertIn(row["ExpectedMessage"], driver.find_element_by_xpath("//*[@id=\"checkout-cart\"]/div[2]").text)
                    except AssertionError as e: self.verificationErrors.append("Hello", str(e))         
    
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
