import random
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_object.base_test import BasePage


class HeaderElements(BasePage):
    """Элементы, которые есть на всех страницах (хедер)"""

    narbar_menu_dropdown = "//li[contains(@class, 'nav-item dropdown')]"

    logo = "//img[contains(@title, 'Your Store')]"

    search_input = "#search input[name='search']"

    search_button = "#search button"

    cart_button = "#header-cart > div > button"

    cart_items_list = "#header-cart > div > ul > li > table > tbody > tr"

    dropdown_currency = "#form-currency > div > a > span"

    list_currency = "#form-currency > div > ul > li"

    current_currency = "#form-currency > div > a > strong"

    my_account_dropdown = "#top > div > div.nav.float-end > ul > li:nth-child(2) > div"

    register_link = "#top > div > div.nav.float-end > ul > li:nth-child(2) > div > ul > li:nth-child(1) > a"

    login_link = "#top > div > div.nav.float-end > ul > li:nth-child(2) > div > ul > li:nth-child(2) > a"

    content = "#content"

    cart = "#header-cart > div > button"

    alert_success = "//div[contains(@class, 'alert-success')]"

    product_show_all = "//div[contains(@class, 'dropdown-menu show')]//a[contains(text(), 'Show All')]"

    narbar_menu = "//nav[contains(@id, 'menu')]"

    @allure.step("Изменение валюты на сайте")
    def change_currency(self, browser, new_currency=None):
        """
        Изменяет текущую валюту на сайте.
        :param browser: WebDriver instance
        :param new_currency: конкретная валюта для выбора (None - случайный выбор)
        :return selected_currency: новая валюта
        """
        with allure.step("1. Открыть dropdown с валютами"):
            self.wait_and_click(browser=browser,
                                target_locator=self.dropdown_currency,
                                method=By.CSS_SELECTOR)

        with allure.step("2. Получить список доступных валют"):
            currencies = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.list_currency)))
            available_currencies = [c.text.strip() for c in currencies]
            allure.attach(
                "\n".join(available_currencies),
                name="Доступные валюты",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Определить текущую валюту"):
            current = self.wait_element(browser,
                                        target_locator=self.current_currency,
                                        method=By.CSS_SELECTOR)
            current_currency = current.text.strip()
            allure.attach(
                current_currency,
                name="Текущая валюта",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(f"4. Выбрать {'указанную' if new_currency else 'случайную'} валюту"):
            selected_currency = new_currency if new_currency else random.choice(
                [c for c in available_currencies if c != current_currency]
            )
            allure.attach(
                selected_currency,
                name="Выбранная валюта",
                attachment_type=allure.attachment_type.TEXT
            )

            for currency in currencies:
                if currency.text.strip() == selected_currency:
                    currency.click()
                    break

        return selected_currency

    @allure.step("Установка масштаба страницы")
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

    @allure.step("Кликнуть на логотип")
    def click_logo(self, browser):
        self.wait_and_click(browser=browser, target_locator=self.logo)
