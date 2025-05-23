from selenium.webdriver.common.by import By

from page_object.main_page import MainPage


class ProductPage(MainPage):
    """Страница конкретного товара"""
    product_title = "h1"
    add_to_cart_btn = "#button-cart"

    def check_elements_product_page(self, browser):
        """Проверка элементовна на странице товара"""
        self.wait_element(browser, target_locator=self.header.logo)
        self.wait_element(browser, target_locator=self.header.search_button, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.search_input, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.content, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.add_to_cart_btn, method=By.CSS_SELECTOR)

    def open_product_page(self, browser):
        """Открытие страницы товара"""
        self.wait_and_click(browser=browser, target_locator=self.first_product, method=By.CSS_SELECTOR)
