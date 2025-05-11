import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class OpencartPO:
    def get_current_product_prices(self, browser, price_selector, count=3):
        """
        Получает текущие цены товаров на странице.
        :param browser: WebDriver instance
        :param price_selector: CSS селектор для элементов с ценами
        :param count: количество цен для возврата (первые N)
        :return: список цен в виде строк
        """
        product_prices = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, price_selector)))
        return [price.text for price in product_prices[:count]]

    def change_currency(self, browser, dropdown_selector, list_selector, current_selector, new_currency=None):
        """
        Изменяет текущую валюту на сайте.
        :param browser: WebDriver instance
        :param dropdown_selector: CSS селектор выпадающего списка валют
        :param list_selector: CSS селектор списка доступных валют
        :param current_selector: CSS селектор текущей валюты
        :param new_currency: конкретная валюта для выбора (None - случайный выбор)
        :return selected_currency: новая валюта
        """
        # Открываем dropdown с валютами
        dropdown = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector)))
        dropdown.click()

        # Получаем список доступных валют
        currencies = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, list_selector)))

        # Определяем текущую валюту
        current = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, current_selector)))
        current_currency = current.text.strip()

        # Выбираем новую валюту
        available_currencies = [c.text.strip() for c in currencies]
        if new_currency:
            selected_currency = new_currency
        else:
            selected_currency = random.choice([c for c in available_currencies if c != current_currency])

        for currency in currencies:
            if currency.text.strip() == selected_currency:
                currency.click()
                break

        return selected_currency

    def verify_currency_changed(self, original_prices, new_prices):
        """
        Проверяет, что цены изменились после смены валюты.
        :param original_prices: список цен до изменения валюты
        :param new_prices: список цен после изменения валюты
        :raises AssertionError: если цены не изменились
        """
        assert original_prices != new_prices, "Цены товаров не изменились после смены валюты"

    def set_page_zoom(self, browser, scale=0.6):
        """
        Устанавливает масштаб страницы.
        :param browser: WebDriver instance
        :param scale: коэффициент масштабирования (0.6 = 60%)
        """
        browser.execute_script(
            f"document.body.style.transform='scale({scale})'; "
            "document.body.style.transformOrigin='0 0'"
        )

    def select_random_menu_item_and_show_all(self, browser, narbar_menu, product_show_all):
        """
        Выбирает случайный пункт меню и нажимает "Показать все" в выбранной категории.

        :param browser: WebDriver instance
        :param narbar_menu: CSS-селектор для элементов главного меню навигации
        :param product_show_all: CSS-селектор кнопки "Показать все" в категории
        """
        # 1. Получаем все пункты меню
        menu_items = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, narbar_menu))
        )

        # 2. Выбираем случайный пункт (исключая первый, если это "Главная")
        select_product = random.choice(menu_items)

        # 3. Кликаем с использованием ActionChains для надежности
        ActionChains(browser).move_to_element(select_product).pause(0.5).click().perform()

        # 4. Кликаем "Показать все" в выбранной категории

        show_all = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, product_show_all))
        )
        show_all.click()
