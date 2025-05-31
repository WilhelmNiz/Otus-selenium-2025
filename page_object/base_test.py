import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def _configure_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Очищаем все существующие обработчики
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Файловый обработчик (перезаписываем файл только при первом запуске)
    file_handler = logging.FileHandler('page_objects.log', mode='w')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


# Вызываем настройку при импорте модуля
_configure_logging()

class BasePage:
    def __init__(self):
        # Просто получаем логгер, настройка уже выполнена
        self.logger = logging.getLogger(self.__class__.__module__ + "." + self.__class__.__name__)

    def wait_and_click(self, browser, target_locator, method=By.XPATH, timeout=10):
        """
        Ожидает кликабельности элемента и выполняет клик по нему.

        :param browser: WebDriver instance - экземпляр браузера
        :param target_locator: str - локатор элемента для поиска
        :param method: By - метод поиска элемента (по умолчанию XPATH)
        :param timeout: int - время ожидания элемента в секундах
        """
        self.logger.info(f"Ожидание и клик по элементу: {target_locator} (метод: {method})")
        try:
            element = WebDriverWait(browser, timeout).until(
                EC.element_to_be_clickable((method, target_locator))
            )
            element.click()
            self.logger.info(f"Успешный клик по элементу: {target_locator}")
        except Exception as e:
            self.logger.error(f"Ошибка при клике по элементу {target_locator}: {str(e)}")
            raise


    def data_entry(self, browser, target, value, method=By.XPATH):
        self.logger.info(f"Ввод данных '{value}' в поле: {target} (метод: {method})")
        try:
            input_target = WebDriverWait(browser, 3).until(
                EC.visibility_of_element_located((method, target)))
            input_target.send_keys(value)
            self.logger.info(f"Успешный ввод данных в поле: {target}")
        except Exception as e:
            self.logger.error(f"Ошибка при вводе данных в поле {target}: {str(e)}")
            raise


    def wait_element(self, browser, target_locator, method=By.XPATH, timeout=10):
        """
        Ожидает плоявление элемента.

        :param browser: WebDriver instance - экземпляр браузера
        :param target_locator: str - локатор элемента для поиска
        :param method: By - метод поиска элемента (по умолчанию XPATH)
        :param timeout: int - время ожидания элемента в секундах
        """
        self.logger.info(f"Ожидание элемента: {target_locator} (метод: {method})")
        try:
            element = WebDriverWait(browser, timeout).until(
                EC.visibility_of_element_located((method, target_locator)))
            self.logger.info(f"Элемент {target_locator} успешно найден")
            return element
        except Exception as e:
            self.logger.error(f"Элемент {target_locator} не найден: {str(e)}")
            raise


    def search_element(self, browser, element, method=By.XPATH):
        self.logger.info(f"Поиск элемента: {element} (метод: {method})")
        try:
            found_element = browser.find_element(method, element).text
            self.logger.info(f"Элемент {element} успешно найден")
            return found_element
        except Exception as e:
            self.logger.error(f"Ошибка при поиске элемента {element}: {str(e)}")
            raise

