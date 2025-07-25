import uuid
import allure

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_object.main_page import MainPage


class AdminPage(MainPage):
    # Админка
    ADMIN_PAGE = "/administration"
    ADMIN_LOGIN_CARD = ".card"
    INPUT_USERNAME = "//input[contains(@name, 'username')]"

    # Кнопка авторизации
    BUTTON_LOGIN = "//button[contains(text(), 'Login')]"

    CARD_HEADER = "#content > div > div > div > div > div.card-header"
    BUTTON_LOGOUT = "#nav-logout > a"

    # Строка с дропдоуном пользователей
    DROPDOWN_CUSTOMERS = "//i[contains (@class, 'fas fa-user')]"

    # Кнопка для перехода в меню редакторования пользователей
    BUTTON_CUSTOMERS = "(//a[contains(text(), 'Customers')])[2]"

    # Инпут "Имя"
    INPUT_FIRSTNAME = "//input[contains(@name, 'firstname')]"

    # Инпут "фамилия"
    INPUT_LASTNAME = "//input[contains(@name, 'lastname')]"

    # Инпут "E-Mail"
    INPUT_E_MAIL = "//input[contains(@name, 'email')]"

    # Инпут "Пароль"
    INPUT_PASSWORD = "//input[contains(@name, 'password')]"

    # Инпут "Подтверждение пароля"
    INPUT_CONFIRM = "//input[contains(@name, 'confirm')]"

    # Кнопка "Сохранить"
    BUTTON_SAVE = "//button[contains(@title, 'Save')]"

    # Инпут Customer Name в фильтрах
    INPUT_CUSTOMER_NAME_FILTER = "//input[contains(@placeholder, 'Customer Name')]"

    # Инпут email в фильтрах
    INPUT_EMAIL_FILTER = "// input[contains( @ placeholder, 'E-Mail')]"

    # Инпут Customer Name
    BUTTON_FILTER = "// button[contains( @ id, 'button-filter')]"

    # Имя пользователя
    CUSTOMER_NAME = "(//td[@class='text-start'])[4]"

    # Имя пользователя
    CUSTOMER_EMAIL = "(//td[@class='text-start'])[5]"

    # КАТАЛОГ(ТОВАРЫ)
    # Строка с дропдоуном "Каталог"
    DROPDOWN_CATALOG = "//i[contains (@class, 'fa-solid fa-tag')]"

    # Кнопка для перехода в меню редактирования товаров
    BUTTON_PRODUCT = "//a[contains (text(), 'Products')]"

    # Инпут имя продукта
    INPUT_PRODUCT_NAME = "//input[contains(@placeholder, 'Product Name')]"

    # Инпут Meta Tag Title
    INPUT_META_TAG_TITLE = "//input[contains(@placeholder, 'Meta Tag Title')]"

    # Раздел "Данные"
    SECTION_DATA = "//a[contains(text(), 'Data')]"

    # Раздел "SEO"
    SECTION_SEO = "(//a[contains(text(), 'SEO')])[2]"

    # Инпут "Ключевое слово"
    INPUT_KEYWORD = "//input[contains(@name, 'seo')]"

    # Инпут модель товара
    INPUT_MODEL = "//input[contains(@placeholder, 'Model')]"

    # Инпут Product Name в фильтрах
    INPUT_PRODUCT_NAME_FILTER = "//input[contains(@placeholder, 'Product Name')]"

    # Инпут Model в фильтрах
    INPUT_MODEL_FILTER = "//input[contains(@placeholder, 'Model')]"

    # Имя товара
    PRODUCT_NAME = "(//td[@class='text-start'])[2]"

    # модель товара
    PRODUCT_MODEL = "(//td[@class='text-start d-none d-lg-table-cell'])[2]"

    # ОБЩЕЕ
    # Кнопка добавления
    BUTTON_ADD_NEW = "//a[contains(@title, 'Add New')]"

    # Чексбокс для выбора всех элементов в списке
    CHECKBOX = "//input[@type='checkbox']"

    # Кнопка "Назад"
    BUTTON_BACK = "//a[contains(@title, 'Back')]"

    # Кнопка "Удалить"
    BUTTON_DELETE = "//button[contains(@title, 'Delete')]"

    # Пустой список элементов
    CLEAR_LIST = "//td[contains (text(), 'No results!')]"

    @allure.step("Авторизация в админ-панели")
    def authorization_admin(self, browser):
        """Выполнение авторизации в административной панели с проверкой успешного входа"""
        self.logger.info("Начало авторизации в админ-панели")

        with allure.step("1. Нажать на кнопку входа в систему"):
            self.logger.info("Клик по кнопке входа в систему")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_LOGIN)

        with allure.step("2. Ввести логин администратора"):
            self.logger.info("Ввод логина администратора: user")
            self.data_entry(browser=browser, target=self.INPUT_USERNAME, value="user")
            allure.attach(
                "user",
                name="Введенный логин",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Ввести пароль администратора"):
            self.logger.info("Ввод пароля администратора")
            self.data_entry(browser=browser, target=self.INPUT_PASSWORD, value="bitnami")
            allure.attach(
                "bitnami",
                name="Введенный пароль",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("4. Подтвердить авторизацию"):
            self.logger.info("Подтверждение авторизации")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_LOGIN)

        with allure.step("5. Проверить успешность авторизации"):
            self.logger.info("Проверка успешности авторизации")
            with allure.step("Убедиться, что заголовок содержит 'Dashboard'"):
                WebDriverWait(browser, 10).until(EC.title_contains("Dashboard"))
                self.logger.info("Авторизация прошла успешно")

    @allure.step("Добавление нового клиента")
    def add_customers(self, browser):
        """Добавление нового клиента в систему с генерацией тестовых данных"""
        self.logger.info("Начало добавления нового клиента")
        id = str(uuid.uuid4())
        email = id + "@test.com"
        value = "Test"

        with allure.step("1. Открыть меню клиентов"):
            self.logger.info("Открытие меню клиентов")
            self.wait_and_click(browser=browser, target_locator=self.DROPDOWN_CUSTOMERS)
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_CUSTOMERS)
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_ADD_NEW)

        with allure.step("2. Проверить переход на страницу клиентов"):
            self.logger.info("Проверка перехода на страницу клиентов")
            assert "Customers" in browser.title, "Не удалось войти в меню редактирования пользователей"
            allure.attach(
                browser.title,
                name="Текущий заголовок страницы",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Заполнить данные клиента"):
            self.logger.info(f"Заполнение данных клиента: {value}")
            self.data_entry(browser=browser, target=self.INPUT_FIRSTNAME, value=value)
            self.data_entry(browser=browser, target=self.INPUT_LASTNAME, value=value)
            self.data_entry(browser=browser, target=self.INPUT_E_MAIL, value=email)
            self.data_entry(browser=browser, target=self.INPUT_PASSWORD, value=value)
            self.data_entry(browser=browser, target=self.INPUT_CONFIRM, value=value)

            allure.attach(
                f"Имя: {value}\nФамилия: {value}\nEmail: {email}\nПароль: {value}",
                name="Введенные данные клиента",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("4. Сохранить клиента"):
            self.logger.info("Сохранение клиента")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_SAVE)
            self.wait_element(browser=browser, target_locator=self.header.ALERT_SUCCESS)

        with allure.step("5. Вернуться к списку клиентов"):
            self.logger.info("Возврат к списку клиентов")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_BACK)

        self.logger.info(f"Клиент успешно добавлен: {value}, {email}")
        return value, email

    @allure.step("Проверка данных пользователя")
    def verifying_user_data(self, browser, firstname, lastname, email):
        """Проверка корректности данных пользователя в системе"""
        self.logger.info(f"Проверка данных пользователя: {firstname} {lastname}, {email}")
        full_name = f"{firstname} {lastname}"

        with allure.step(f"1. Заполнить фильтр для поиска пользователя {full_name}"):
            self.logger.info(f"Заполнение фильтра для поиска: {full_name}, {email}")
            self.data_entry(browser=browser, target=self.INPUT_CUSTOMER_NAME_FILTER, value=full_name)
            self.data_entry(browser=browser, target=self.INPUT_EMAIL_FILTER, value=email)
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_FILTER)

            allure.attach(
                f"Фильтр по имени: {full_name}\nФильтр по email: {email}",
                name="Параметры поиска",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2. Получить данные найденного пользователя"):
            self.logger.info("Получение данных найденного пользователя")
            name = self.search_element(browser, element=self.CUSTOMER_NAME)
            clean_name = name.replace("Enabled", "").strip()
            mail = self.search_element(browser, element=self.CUSTOMER_EMAIL)

            allure.attach(
                f"Найденное имя: {clean_name}\nНайденный email: {mail}",
                name="Фактические данные пользователя",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Проверить соответствие данных"):
            self.logger.info("Проверка соответствия данных")
            assert full_name == clean_name, f"Ожидалось имя: {full_name}, получено: {clean_name}"
            assert email == mail, f"Ожидался email: {email}, получен: {mail}"
            self.logger.info("Данные пользователя совпадают")

            allure.attach(
                "Все данные пользователя совпадают",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.step("Добавление нового товара")
    def add_product(self, browser):
        """Добавление нового тестового товара в каталог"""
        self.logger.info("Начало добавления нового товара")
        id = str(uuid.uuid4())
        value = "Test" + id

        with allure.step("1. Открыть раздел каталога"):
            self.logger.info("Открытие раздела каталога")
            self.wait_and_click(browser=browser, target_locator=self.DROPDOWN_CATALOG)
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_PRODUCT)
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_ADD_NEW)

        with allure.step("2. Проверить переход на страницу товаров"):
            self.logger.info("Проверка перехода на страницу товаров")
            assert "Products" in browser.title, "Не удалось войти в меню редактирования товаров"
            allure.attach(
                browser.title,
                name="Текущий заголовок страницы",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Заполнить основные данные товара"):
            self.logger.info(f"Заполнение основных данных товара: {value}")
            self.data_entry(browser=browser, target=self.INPUT_PRODUCT_NAME, value=value)
            self.data_entry(browser=browser, target=self.INPUT_META_TAG_TITLE, value=value)
            allure.attach(
                f"Название товара: {value}\nMeta-тег Title: {value}",
                name="Основные данные товара",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("4. Заполнить данные в разделе Data"):
            self.logger.info("Заполнение данных в разделе Data")
            self.wait_and_click(browser=browser, target_locator=self.SECTION_DATA)
            self.data_entry(browser=browser, target=self.INPUT_MODEL, value=value)
            allure.attach(
                f"Модель товара: {value}",
                name="Технические характеристики",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("5. Заполнить SEO-параметры"):
            self.logger.info("Заполнение SEO-параметров")
            self.wait_and_click(browser=browser, target_locator=self.SECTION_SEO)
            self.data_entry(browser=browser, target=self.INPUT_KEYWORD, value=id)
            allure.attach(
                f"SEO Keyword: {id}",
                name="SEO-настройки",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("6. Сохранить товар"):
            self.logger.info("Сохранение товара")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_SAVE)
            self.wait_element(browser, target_locator=self.header.ALERT_SUCCESS)
            allure.attach(
                "Товар успешно сохранен",
                name="Результат сохранения",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("7. Вернуться к списку товаров"):
            self.logger.info("Возврат к списку товаров")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_BACK)

        self.logger.info(f"Товар успешно добавлен: {value}")
        return value

    @allure.step("Проверка данных товара")
    def verifying_product_data(self, browser, value):
        """Проверка корректности данных товара в системе"""
        self.logger.info(f"Проверка данных товара: {value}")

        with allure.step(f"1. Применить фильтр для поиска товара '{value}'"):
            self.logger.info(f"Применение фильтра для поиска товара: {value}")
            self.data_entry(browser=browser, target=self.INPUT_PRODUCT_NAME_FILTER, value=value)
            self.data_entry(browser=browser, target=self.INPUT_MODEL_FILTER, value=value)
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_FILTER)

            allure.attach(
                f"Фильтр по названию: {value}\nФильтр по модели: {value}",
                name="Параметры фильтрации",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("2. Получить фактические данные товара"):
            self.logger.info("Получение фактических данных товара")
            name_product = self.wait_element(browser, target_locator=self.PRODUCT_NAME)
            name_product = name_product.text
            clean_name = name_product.replace("Enabled", "").strip()
            model = self.wait_element(browser, target_locator=self.PRODUCT_MODEL)
            model = model.text

            allure.attach(
                f"Найденное название: {clean_name}\nНайденная модель: {model}",
                name="Фактические данные",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("3. Проверить соответствие данных"):
            self.logger.info("Проверка соответствия данных товара")
            assert value == clean_name, f"Ожидалось название: '{value}', получено: '{clean_name}'"
            assert value == model, f"Ожидалась модель: '{value}', получено: '{model}'"
            self.logger.info("Данные товара соответствуют ожидаемым")

            allure.attach(
                "Все данные товара соответствуют ожидаемым",
                name="Результат проверки",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.step("Удаление товара из системы")
    def delete_product(self, browser):
        """Удаление товара с подтверждением операции"""
        self.logger.info("Начало удаления товара")

        with allure.step("1. Выбрать товар для удаления"):
            self.logger.info("Выбор товара для удаления")
            self.wait_and_click(browser=browser, target_locator=self.CHECKBOX)

        with allure.step("2. Нажать кнопку удаления"):
            self.logger.info("Нажатие кнопки удаления")
            self.wait_and_click(browser=browser, target_locator=self.BUTTON_DELETE)

        with allure.step("3. Подтвердить удаление в диалоговом окне"):
            self.logger.info("Подтверждение удаления")
            alert = Alert(browser)
            alert.accept()
            allure.attach(
                "Удаление подтверждено",
                name="Подтверждение",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("4. Проверить очистку списка товаров"):
            self.logger.info("Проверка очистки списка товаров")
            self.search_element(browser, element=self.CLEAR_LIST)
            allure.attach(
                "Список товаров очищен",
                name="Результат удаления",
                attachment_type=allure.attachment_type.TEXT
            )

        self.logger.info("Товар успешно удален")

    @allure.step("Проверка элементов на странице администрирования")
    def check_elements_admin_page(self, browser):
        """Проверка наличия основных элементов на странице входа в админ-панель"""
        self.logger.info("Проверка элементов на странице администрирования")

        with allure.step("1. Проверить наличие карточки авторизации"):
            self.logger.info("Проверка карточки авторизации")
            self.wait_element(browser, target_locator=self.ADMIN_LOGIN_CARD, method=By.CSS_SELECTOR)

        with allure.step("2. Проверить поле ввода пароля"):
            self.logger.info("Проверка поля ввода пароля")
            self.wait_element(browser, target_locator=self.INPUT_PASSWORD)

        with allure.step("3. Проверить поле ввода логина"):
            self.logger.info("Проверка поля ввода логина")
            self.wait_element(browser, target_locator=self.INPUT_USERNAME)

        with allure.step("4. Проверить кнопку входа"):
            self.logger.info("Проверка кнопки входа")
            self.wait_element(browser, target_locator=self.BUTTON_LOGIN)

        with allure.step("5. Проверить заголовок карточки авторизации"):
            self.logger.info("Проверка заголовка карточки авторизации")
            self.wait_element(browser, target_locator=self.CARD_HEADER, method=By.CSS_SELECTOR)

        self.logger.info("Все элементы на странице администрирования присутствуют")

    @allure.step("Выход из административной панели")
    def logout(self, browser):
        """Выполнение выхода из административной панели с проверкой успешного разлогина"""
        self.logger.info("Начало выхода из административной панели")

        with allure.step("1. Нажать кнопку выхода из системы"):
            self.logger.info("Нажатие кнопки выхода из системы")
            self.wait_and_click(browser=browser,
                              target_locator=self.BUTTON_LOGOUT,
                              method=By.CSS_SELECTOR)

        with allure.step("2. Проверить появление формы авторизации"):
            self.logger.info("Проверка появления формы авторизации")
            self.wait_element(browser,
                            target_locator=self.ADMIN_LOGIN_CARD,
                            method=By.CSS_SELECTOR)

        with allure.step("3. Проверить заголовок страницы"):
            self.logger.info("Проверка заголовка страницы")
            current_title = browser.title
            assert "Administration" in current_title, \
                f"Не удалось выйти из админки. Текущий заголовок: {current_title}"

        self.logger.info("Выход из административной панели выполнен успешно")