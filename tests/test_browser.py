import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from page_object.opencart import OpencartElements
from opencart_po import OpencartPO


def test_opencart_check_title(browser, base_url):
    """Тест проверки основных элементов главной страницы"""
    elem = OpencartElements()
    browser.get(base_url)
    WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.logo)))
    WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.search_input)))
    WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.cart)))
    WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.carousel_banner)))
    WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.navbar_menu)))


def test_opencart_catalog(browser, base_url):
    """Тест проверки элементов каталога товаров"""
    elem = OpencartElements()
    op = OpencartPO()
    browser.get(base_url)
    op.select_random_menu_item_and_show_all(browser, narbar_menu=elem.narbar_menu,
                                            product_show_all=elem.product_show_all)

    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.product_list)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.search_button)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.search_input)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.logo)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.product_name)))


def test_opencart_product(browser, base_url):
    """Тест проверки элементов страницы товара"""
    elem = OpencartElements()
    browser.get(base_url)
    product = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, elem.first_product)))
    product.click()
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.content)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.search_button)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.search_input)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.logo)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.add_to_cart_btn)))


def test_opencart_check_admin(browser, base_url):
    """Тест проверки элементов страницы администрирования"""
    elem = OpencartElements()
    browser.get(base_url + elem.admin_page)
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.admin_login_card)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.input_password)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.input_username)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.button_login)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.card_header)))


def test_opencart_register(browser, base_url):
    """Тест проверки элементов страницы регистрации"""
    elem = OpencartElements()
    browser.get(base_url)
    dropdown = WebDriverWait(browser, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, elem.my_account_dropdown)))
    dropdown.click()

    register = WebDriverWait(browser, 3).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, elem.register_link)))
    register.click()
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.register_form)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.firstname_input)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.lastname_input)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.email_input)))
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, elem.register_form)))


def test_admin_login_logout(browser, base_url):
    """Тест авторизации и выхода из админ-панели"""
    elem = OpencartElements()

    browser.get(base_url + elem.admin_page)

    button_login = browser.find_element(By.CSS_SELECTOR, elem.button_login)
    button_login.click()  # по какой-то причине не удается при первой попытке залогиниться, поэтому добавлено это действие.

    input_username = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, elem.input_username)))
    input_username.send_keys("user")
    input_password = WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, elem.input_password)))
    input_password.send_keys("bitnami")

    button_login = browser.find_element(By.CSS_SELECTOR, elem.button_login)
    button_login.click()

    WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1"))
    )
    assert "Dashboard" in browser.title, "Не удалось войти в админку"

    logout_button = WebDriverWait(browser, 3).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, elem.button_logout))
    )
    logout_button.click()

    WebDriverWait(browser, 3).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, elem.admin_login_card))
    )
    assert "Administration" in browser.title, "Не удалось выйти из админки"


def test_add_random_product_to_cart(browser, base_url):
    """Тест добавления товара в корзину"""
    elem = OpencartElements()
    op = OpencartPO()
    browser.get(base_url)
    logo = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, elem.logo))
    )
    logo.click()
    op.set_page_zoom(browser)

    all_products = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, elem.all_product_name))
    )

    random_product = random.choice(all_products)

    product_name = random_product.find_element(By.CSS_SELECTOR, elem.title_product_name).text

    add_button = WebDriverWait(random_product, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, elem.button_add_to_cart))
    )
    add_button.click()

    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, elem.alert_success))
    )
    WebDriverWait(browser, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, elem.alert_success))
    )
    cart_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, elem.cart))
    )

    cart_button.click()

    items_in_cart = browser.find_elements(By.CSS_SELECTOR, elem.list_of_products_in_cart)
    assert len(items_in_cart) > 0, "Корзина пуста"

    found = False
    for item in items_in_cart:
        if product_name in item.text:
            found = True
            break

    assert found, f"Товар '{product_name}' не найден в корзине"


def test_select_currency_title(browser, base_url):
    """Тест смены валюты на главной странице"""
    elem = OpencartElements()
    op = OpencartPO()
    browser.get(base_url)

    logo = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, elem.logo))
    )
    logo.click()

    op.set_page_zoom(browser)

    prices_before = op.get_current_product_prices(browser, price_selector=elem.price)

    new_currency = op.change_currency(browser, dropdown_selector=elem.dropdown_currency,
                                      list_selector=elem.list_currency, current_selector=elem.current_currency)

    op.set_page_zoom(browser)

    op.verify_currency_changed(original_prices=prices_before, new_prices=new_currency)


def test_select_currency_catalog(browser, base_url):
    """Тест смены валюты в каталоге"""
    elem = OpencartElements()
    op = OpencartPO()
    browser.get(base_url)
    op.select_random_menu_item_and_show_all(browser, narbar_menu=elem.narbar_menu,
                                            product_show_all=elem.product_show_all)

    prices_before = op.get_current_product_prices(browser, price_selector=elem.price)

    new_currency = op.change_currency(browser, dropdown_selector=elem.dropdown_currency,
                                      list_selector=elem.list_currency, current_selector=elem.current_currency)

    op.set_page_zoom(browser)

    op.verify_currency_changed(original_prices=prices_before, new_prices=new_currency)
