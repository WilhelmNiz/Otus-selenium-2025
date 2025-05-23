import pytest
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
