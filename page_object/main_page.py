import random
from page_object.base_test import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_object.header_elements import HeaderElements


class MainPage(BasePage):
    """Главная страница OpenCart"""
    carousel_banner = "#carousel-banner-0"
    all_product_name = ".product-thumb"
    title_product_name = "h4 a"
    button_add_to_cart = "button[formaction*='cart.add']"
    first_product = ".product-thumb:first-child"

    def __init__(self):
        super().__init__()
        self.header = HeaderElements()

    def add_product_cart(self, browser):
        """Добавление товара в корзину"""
        all_products = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.all_product_name))
        )

        random_product = random.choice(all_products)

        product_name = random_product.find_element(By.CSS_SELECTOR, self.title_product_name).text

        self.wait_and_click(browser=browser, target_locator=self.button_add_to_cart, method=By.CSS_SELECTOR)

        self.wait_element(browser, target_locator=self.header.alert_success)

        self.wait_and_click(browser=browser, target_locator=self.header.cart, method=By.CSS_SELECTOR)

        return product_name

    def checking_product_cart(self, browser, product_name):
        """Проверка товара в корзине"""
        items_in_cart = browser.find_elements(By.CSS_SELECTOR, self.header.cart_items_list)
        assert len(items_in_cart) > 0, "Корзина пуста"

        found = False
        for item in items_in_cart:
            if product_name in item.text:
                found = True
                break

        assert found, f"Товар '{product_name}' не найден в корзине"

    def check_elements_main_page(self, browser):
        """Проверка элементовна на главной странице"""
        self.wait_element(browser, target_locator=self.header.logo)
        self.wait_element(browser, target_locator=self.header.search_input, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.cart, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.carousel_banner, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.narbar_menu)
