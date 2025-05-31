import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFoptions
from selenium.webdriver.chrome.options import Options as CHoptions

def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests")
    parser.addoption("--headless", action = "store_true", help="Activate headless mode")
    parser.addoption("--url", "-U", help="Base application url", default="localhost:8081/")


@pytest.fixture()
def browser(request):
    driver = None
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    url = request.config.getoption("--url")

    if browser_name in ["ch", "chrome"]:
        options = CHoptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(options=options)

    elif browser_name in ["ff", "firefox"]:
        options = FFoptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    request.addfinalizer(driver.quit)

    def open(path=""):
        return driver.get(url + path)

    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.open = open
    driver.open()

    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Делаем скриншот только при падении теста
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver is not None:
            try:
                # Добавляем скриншот в отчет
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )

                # Дополнительно можно добавить исходный код страницы
                allure.attach(
                    driver.page_source,
                    name="page_source",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")