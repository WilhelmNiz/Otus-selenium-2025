from selenium.webdriver.common.by import By

from page_object.main_page import MainPage


class AuthPage(MainPage):
    """Страницы входа и регистрации"""
    firstname_input = "#input-firstname"
    lastname_input = "#input-lastname"
    email_input = "#input-email"
    register_form = "#form-register > div > button"
    input_password = "#input-password"
    input_username = "#input-username"
    button_login = "#form-login > div.text-end > button"
    card_header = "#content > div > div > div > div > div.card-header"
    button_logout = "#nav-logout > a"

    def check_elements_auth_page(self, browser):
        """Проверка элементов на странице авторизации"""
        self.logger.info("Проверка элементов на странице авторизации")

        self.logger.info("Проверка наличия логотипа")
        self.wait_element(browser, target_locator=self.header.logo)

        self.logger.info("Проверка поля ввода имени")
        self.wait_element(browser, target_locator=self.firstname_input, method=By.CSS_SELECTOR)

        self.logger.info("Проверка поля ввода фамилии")
        self.wait_element(browser, target_locator=self.lastname_input, method=By.CSS_SELECTOR)

        self.logger.info("Проверка поля ввода email")
        self.wait_element(browser, target_locator=self.email_input, method=By.CSS_SELECTOR)

        self.logger.info("Проверка формы регистрации")
        self.wait_element(browser, target_locator=self.register_form, method=By.CSS_SELECTOR)

        self.logger.info("Все элементы на странице авторизации присутствуют")

    def open_auth_page(self, browser):
        """Открытие страницы регистрации"""
        self.logger.info("Открытие страницы регистрации")

        self.logger.info("Клик по выпадающему меню 'Мой аккаунт'")
        self.wait_and_click(
            browser=browser,
            target_locator=self.header.my_account_dropdown,
            method=By.CSS_SELECTOR
        )

        self.logger.info("Клик по ссылке 'Регистрация'")
        self.wait_and_click(
            browser=browser,
            target_locator=self.header.register_link,
            method=By.CSS_SELECTOR
        )

        self.logger.info("Страница регистрации успешно открыта")