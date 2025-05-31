import uuid

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

from page_object.main_page import MainPage


class AdminPage(MainPage):
    # Админка
    admin_page = "/administration"
    admin_login_card = ".card"
    input_username = "//input[contains(@name, 'username')]"

    # Кнопка авторизации
    button_login = "//button[contains(text(), 'Login')]"

    card_header = "#content > div > div > div > div > div.card-header"
    button_logout = "#nav-logout > a"

    # Строка с дропдоуном пользователей
    dropdown_customers = "//i[contains (@class, 'fas fa-user')]"

    # Кнопка для перехода в меню редакторования пользователей
    button_customers = "(//a[contains(text(), 'Customers')])[2]"

    # Инпут "Имя"
    input_firstname = "//input[contains(@name, 'firstname')]"

    # Инпут "фамилия"
    input_lastname = "//input[contains(@name, 'lastname')]"

    # Инпут "E-Mail"
    input_e_mail = "//input[contains(@name, 'email')]"

    # Инпут "Пароль"
    input_password = "//input[contains(@name, 'password')]"

    # Инпут "Подтверждение пароля"
    input_confirm = "//input[contains(@name, 'confirm')]"

    # Кнопка "Сохранить"
    button_save = "//button[contains(@title, 'Save')]"

    # Инпут Customer Name в фильтрах
    input_customer_name_filter = "//input[contains(@placeholder, 'Customer Name')]"

    # Инпут email в фильтрах
    input_email_filter = "// input[contains( @ placeholder, 'E-Mail')]"

    # Инпут Customer Name
    button_filter = "// button[contains( @ id, 'button-filter')]"

    #Имя пользователя
    customer_name = "(//td[@class='text-start'])[4]"

    # Имя пользователя
    customer_email = "(//td[@class='text-start'])[5]"

    #КАТАЛОГ(ТОВАРЫ)
    # Строка с дропдоуном "Каталог"
    dropdown_catalog = "//i[contains (@class, 'fa-solid fa-tag')]"

    # Кнопка для перехода в меню редактирования товаров
    button_product = "//a[contains (text(), 'Products')]"

    # Инпут имя продукта
    input_product_name = "//input[contains(@placeholder, 'Product Name')]"

    # Инпут Meta Tag Title
    input_meta_tag_title = "//input[contains(@placeholder, 'Meta Tag Title')]"

    # Раздел "Данные"
    section_data = "//a[contains(text(), 'Data')]"

    # Раздел "SEO"
    section_seo = "(//a[contains(text(), 'SEO')])[2]"

    # Инпут "Ключевое слово"
    input_keyword= "//input[contains(@name, 'seo')]"

    # Инпут модель товара
    input_model = "//input[contains(@placeholder, 'Model')]"

    # Инпут Product Name в фильтрах
    input_product_name_filter = "//input[contains(@placeholder, 'Product Name')]"

    # Инпут Model в фильтрах
    input_model_filter = "//input[contains(@placeholder, 'Model')]"

    # Имя товара
    product_name = "(//td[@class='text-start'])[2]"

    # модель товара
    product_model = "(//td[@class='text-start d-none d-lg-table-cell'])[2]"

    # ОБЩЕЕ
    # Кнопка добавления
    button_add_new = "//a[contains(@title, 'Add New')]"

    # Чексбокс для выбора всех элементов в списке
    checkbox = "//input[@type='checkbox']"

    # Кнопка "Назад"
    button_back = "//a[contains(@title, 'Back')]"

    # Кнопка "Удалить"
    button_delete = "//button[contains(@title, 'Delete')]"

    # Пустой список элементов
    clear_list = "//td[contains (text(), 'No results!')]"


    def authorization_admin(self, browser):
        """Авторизация в админ-панели"""
        self.wait_and_click(browser=browser, target_locator=self.button_login)

        self.data_entry(browser = browser, target = self.input_username, value ="user")

        self.data_entry(browser=browser, target=self.input_password, value="bitnami")

        self.wait_and_click(browser=browser, target_locator=self.button_login)

        assert "Dashboard" in browser.title, "Не удалось войти в меню редакторования пользователей"

    def add_customers(self, browser):
        id = str(uuid.uuid4())
        email = id + "@test.com"
        value = "Test"
        self.wait_and_click(browser=browser, target_locator=self.dropdown_customers)

        self.wait_and_click(browser=browser, target_locator=self.button_customers)

        self.wait_and_click(browser=browser, target_locator=self.button_add_new)

        assert "Customers" in browser.title, "Не удалось войти в админку"

        self.data_entry(browser=browser, target=self.input_firstname, value=value)

        self.data_entry(browser=browser, target=self.input_lastname, value=value)

        self.data_entry(browser=browser, target=self.input_e_mail, value=email)

        self.data_entry(browser=browser, target=self.input_password, value=value)

        self.data_entry(browser=browser, target=self.input_confirm, value=value)

        self.wait_and_click(browser=browser, target_locator=self.button_save)

        self.wait_element(browser=browser, target_locator = self.header.alert_success)

        self.wait_and_click(browser=browser, target_locator=self.button_back)

        return value, email


    def verifying_user_data(self, browser, firstname, lastname, email):
        full_name = f"{firstname} {lastname}"

        self.data_entry(browser=browser, target=self.input_customer_name_filter, value=full_name)
        self.data_entry(browser=browser, target=self.input_email_filter, value=email)
        self.wait_and_click(browser=browser, target_locator=self.button_filter)
        name = self.search_element(browser, element = self.customer_name)
        name = name.replace("Enabled", "").strip()
        mail = self.search_element(browser, element=self.customer_email)
        assert full_name == name
        assert email == mail

    def add_product(self, browser):
        id = str(uuid.uuid4())
        value = "Test" + id
        self.wait_and_click(browser=browser, target_locator=self.dropdown_catalog)

        self.wait_and_click(browser=browser, target_locator=self.button_product)

        self.wait_and_click(browser=browser, target_locator=self.button_add_new)

        assert "Products" in browser.title, "Не удалось войти в меню редакторования товаров"

        self.data_entry(browser=browser, target=self.input_product_name, value=value)

        self.data_entry(browser=browser, target=self.input_meta_tag_title, value=value)

        self.wait_and_click(browser=browser, target_locator=self.section_data)

        self.data_entry(browser=browser, target=self.input_model, value=value)

        self.wait_and_click(browser=browser, target_locator=self.section_seo)

        self.data_entry(browser=browser, target=self.input_keyword, value=id)

        self.wait_and_click(browser=browser, target_locator=self.button_save)

        self.wait_element(browser, target_locator = self.header.alert_success)

        self.wait_and_click(browser=browser, target_locator=self.button_back)

        return value

    def verifying_product_data(self, browser, value):

        self.data_entry(browser=browser, target=self.input_product_name_filter, value=value)
        self.data_entry(browser=browser, target=self.input_model_filter, value=value)
        self.wait_and_click(browser=browser, target_locator=self.button_filter)
        name_product = self.search_element(browser, element=self.product_name)
        name_product = name_product.replace("Enabled", "").strip()
        model = self.search_element(browser, element=self.product_model)
        assert value == name_product
        assert value == model

    def delete_product(self, browser):
        """Удаление продукта"""
        self.wait_and_click(browser=browser, target_locator=self.checkbox)
        self.wait_and_click(browser=browser, target_locator=self.button_delete)
        alert = Alert(browser)
        alert.accept()
        self.search_element(browser, element=self.clear_list)


    def check_elements_admin_page(self, browser):
        """Проверка элементовна на странице администрирования"""
        self.wait_element(browser, target_locator=self.admin_login_card, method=By.CSS_SELECTOR)
        self.wait_element(browser, target_locator=self.input_password)
        self.wait_element(browser, target_locator=self.input_username)
        self.wait_element(browser, target_locator=self.button_login)
        self.wait_element(browser, target_locator=self.card_header, method=By.CSS_SELECTOR)

    def logout(self, browser):
        """Выход из админки"""
        self.wait_and_click(browser=browser, target_locator=self.button_logout, method=By.CSS_SELECTOR)

        self.wait_element(browser, target_locator =self.admin_login_card, method=By.CSS_SELECTOR)

        assert "Administration" in browser.title, "Не удалось выйти из админки"

