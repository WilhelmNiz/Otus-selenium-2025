import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFoptions
from selenium.webdriver.chrome.options import Options as CHoptions

def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests")
    parser.addoption("--headless", action = "store_true", help="Activate headless mode")
    parser.addoption("--base_url", help="Base application url", default="localhost:8081/")

@pytest.fixture()
def base_url(request):
    return  "http://" + request.config.getoption("--base_url")


@pytest.fixture()
def browser(request):
    driver = None
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

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

    yield driver

    driver.quit()