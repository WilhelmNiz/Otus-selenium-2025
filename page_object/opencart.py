class OpencartNavigation:
    """Класс для навигации по страницам OpenCart"""

    def __init__(self):
        self.narbar_menu = "#narbar-menu > ul > li:nth-child(1) > a"
        self.product_show_all = "a.see-all"

        self.my_account_dropdown = "#top > div > div.nav.float-end > ul > li:nth-child(2) > div"
        self.register_link = "#top > div > div.nav.float-end > ul > li:nth-child(2) > div > ul > li:nth-child(1) > a"
        self.login_link = "#top > div > div.nav.float-end > ul > li:nth-child(2) > div > ul > li:nth-child(2) > a"

        self.admin_page = "/administration"

        self.first_product = ".product-thumb:first-child"


class OpencartElements(OpencartNavigation):
    """Класс с элементами страниц OpenCart"""

    def __init__(self):
        super().__init__()
        # Общие элементы
        self.logo = "#logo"
        self.search_input = "#search input[name='search']"
        self.search_button = "#search button"
        self.cart = "#header-cart > div > button"
        self.list_of_products_in_cart = "#header-cart > div > ul > li > table > tbody > tr"
        self.content = "#content"
        self.price = "div.price"
        self.dropdown_currency = "#form-currency > div > a > span"
        self.list_currency = "#form-currency > div > ul > li"
        self.current_currency = "#form-currency > div > a > strong"

        # Главная страница
        self.carousel_banner = "#carousel-banner-0"
        self.navbar_menu = "#narbar-menu"
        self.all_product_name = ".product-thumb"
        self.title_product_name = "h4 a"
        self.button_add_to_cart = "button[formaction*='cart.add']"

        # Каталог
        self.product_list = "#product-list"
        self.product_name = ".product-thumb h4 a"

        # Страница товара
        self.product_title = "h1"
        self.add_to_cart_btn = "#button-cart"

        # Регистрация
        self.register_form = "#form-register"
        self.firstname_input = "#input-firstname"
        self.lastname_input = "#input-lastname"
        self.email_input = "#input-email"
        self.register_form = "#form-register > div > button"
