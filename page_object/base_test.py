from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:

    def wait_and_click(self, browser, target_locator, method=By.XPATH, timeout=10):
        """
        Ожидает кликабельности элемента и выполняет клик по нему.

        :param browser: WebDriver instance - экземпляр браузера
        :param target_locator: str - локатор элемента для поиска
        :param method: By - метод поиска элемента (по умолчанию XPATH)
        :param timeout: int - время ожидания элемента в секундах
        """
        element = WebDriverWait(browser, timeout).until(
            EC.element_to_be_clickable((method, target_locator))
        )
        element.click()

    def data_entry(self, browser, target, value, method=By.XPATH):
        input_target = WebDriverWait(browser, 3).until(
            EC.visibility_of_element_located((method, target)))
        input_target.send_keys(value)


    def wait_element(self, browser, target_locator, method=By.XPATH, timeout=10):
        """
        Ожидает плоявление элемента.

        :param browser: WebDriver instance - экземпляр браузера
        :param target_locator: str - локатор элемента для поиска
        :param method: By - метод поиска элемента (по умолчанию XPATH)
        :param timeout: int - время ожидания элемента в секундах
        """
        return WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((method, target_locator))
        )


    def search_element(self, browser, element, method=By.XPATH):

        return browser.find_element(method, element).text

