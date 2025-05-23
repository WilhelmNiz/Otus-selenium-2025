import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_object.main_page import MainPage


class CatalogPage(MainPage):
    """Страница каталога товаров"""

    # Путь до цен товаров
    price = "div.price"

    # Путь до списка товаров
    product_list = "#product-list"

    # Путь до наименований товаров
    product_name = ".product-thumb h4 a"

    def select_random_menu_item_and_show_all(self, browser):
        """
        Выбирает случайный пункт меню и нажимает "Показать все" в выбранной категории.

        :param browser: WebDriver instance
        """
        # 1. Получаем все пункты меню
        menu_items = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, self.header.narbar_menu_dropdown))
        )

        # 2. Выбираем случайный пункт
        select_product = random.choice(menu_items)
        # 3. Кликаем на случайный пункт меню
        select_product.click()

        # 4. Кликаем "Показать все" в выбранной категории
        self.wait_and_click(browser=browser, target_locator=self.header.product_show_all)

    def get_current_product_prices(self, browser, count=3):
        """
        Получает текущие цены товаров на странице.
        :param browser: WebDriver instance
        :param count: количество цен для возврата (первые N)
        :return: список цен в виде строк
        """
        product_prices = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.price)))
        return [price.text for price in product_prices[:count]]

    def verify_currency_changed(self, original_prices, new_prices):
        """
        Проверяет, что цены изменились после смены валюты.
        :param original_prices: список цен до изменения валюты
        :param new_prices: список цен после изменения валюты
        :raises AssertionError: если цены не изменились
        """
        assert original_prices != new_prices, "Цены товаров не изменились после смены валюты"

    def check_elements_catalog_page(self, browser):
        """Проверка элементовна в каталоге"""
        self.wait_element(browser, target_locator=self.product_list, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.search_button, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.search_input, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.header.logo)
        self.wait_element(browser, target_locator=self.product_name, method=By.CSS_SELECTOR)