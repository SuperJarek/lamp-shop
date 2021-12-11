import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShopScraper:

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='/home/zula/Downloads/geckodriver-v0.30.0-linux32/geckodriver')

    def close(self):
        self.driver.close()

    def start_scraper(self):
        self.driver.get("http://localhost/")
        signup_button = self.driver.find_element(By.XPATH, '//div[@class="user-info"]/a')
        signup_button.click()
        new_account_button = self.driver.find_element(By.XPATH, '//div[@class="no-account"]/a')
        new_account_button.click()
        self.fill_signup_form()
        self.select_all_products()
        self.fill_basket()
        self.remove_product_from_shopping_cart()
        self.checkout_the_order()
        self.fill_order_form()
        self.check_order_status()
        self.close()

    def fill_signup_form(self):
        self.driver.find_element(By.XPATH, '//span[@class="custom-radio"]/input').click()
        first_name_field = self.driver.find_element(By.NAME, 'firstname')
        first_name_field.send_keys('name')
        last_name_field = self.driver.find_element(By.NAME, 'lastname')
        last_name_field.send_keys('surname')
        email_field = self.driver.find_element(By.NAME, 'email')
        email_field.send_keys('email1@email.com')
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys('admin123')
        self.driver.find_element(By.NAME, 'psgdpr').click()
        self.driver.find_element(By.XPATH, '//footer[@class="form-footer clearfix"]/button').click()

    def fill_basket(self):
        category_links = [link.get_attribute('href') for link in self.driver.find_elements(By.XPATH, '//ul[@class="category-top-menu"]/li[2]/ul/li/a')]
        for link in category_links[:2]:
            self.driver.get(link)
            self.add_products()
            self.driver.back()

    def add_products(self):
        all_products = self.driver.find_elements(By.XPATH, '//div[@class="products row"]/article/div/a')
        product_links = [link.get_attribute('href') for link in all_products]
        for product_link in product_links[:5]:
            time.sleep(1)
            self.driver.get(product_link)
            self.set_product_quantity()

    def set_product_quantity(self):
        quantity_element = self.driver.find_element(By.XPATH, '//div[@class="product-quantity clearfix"]')
        for _ in range(0, random.randint(1, 5)):
            quantity_element.find_element(By.XPATH, './/i[@class="material-icons touchspin-up"]').click()

        quantity_element.find_element(By.XPATH, './/button[@class="btn btn-primary add-to-cart"]').click()
        time.sleep(1)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@class="modal-dialog"]//button[@class="btn btn-secondary"]'))).click()

        self.driver.back()

    def set_product_variant(self):
        try:
            all_options = self.driver.find_elements(By.XPATH, '//div[@class="product-variants"]//select/option')
            self.driver.find_element(By.XPATH, '//div[@class="product-variants"]//select').click()
            chosen_option = random.randint(1, len(all_options))
            all_options[chosen_option - 1].click()
        except NoSuchElementException:
            pass

    def remove_product_from_shopping_cart(self):
        self.driver.find_element(By.XPATH, '//div[@id="_desktop_cart"]//a').click()
        self.driver.find_element(By.XPATH, '//div[@class="card cart-container"]//ul[@class="cart-items"]/li//a[@class="remove-from-cart"]').click()

    def checkout_the_order(self):
        self.driver.find_element(By.XPATH, '//div[contains(@class, "checkout cart")]//a').click()

    def fill_order_form(self):
        address = self.driver.find_element(By.NAME, 'address1')
        address.send_keys('address')
        postcode = self.driver.find_element(By.NAME, 'postcode')
        postcode.send_keys('83-110')
        city = self.driver.find_element(By.NAME, 'city')
        city.send_keys('Gdansk')
        self.driver.find_element(By.XPATH, '//footer[@class="form-footer clearfix"]/button').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//button[@name="confirmDeliveryOption"]').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//div[contains(@id, "payment-option-1")]/span/input').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//form[@id="conditions-to-approve"]/ul/li/div/span/input').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//div[@id="payment-confirmation"]/div/button').click()
        time.sleep(1)

    def check_order_status(self):
        self.driver.find_element(By.XPATH, '//div[@class="user-info"]/a[@class="account"]').click()
        self.driver.find_element(By.XPATH, '//a[@id="history-link"]').click()
        self.driver.find_element(By.XPATH, '//td[contains(@class, "order-actions")]/a').click()

    def select_all_products(self):
        self.driver.find_element(By.XPATH, '//a[contains(@class, "all-product-link")]').click()
        self.driver.find_element(By.XPATH, '//a[contains(text(), "Dekoracja")]').click()
        self.driver.find_element(By.XPATH, '//a[contains(text(), "Oświetlenie")]').click()


if __name__ == '__main__':
    scraper = ShopScraper()
    scraper.start_scraper()
