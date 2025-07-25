import pytest
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFoptions
from selenium.webdriver.chrome.options import Options as CHoptions


def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests")
    parser.addoption("--headless", action="store_true", help="Activate headless mode")
    parser.addoption("--url", "-U", help="Base application url", default="http://localhost:8081/")
    parser.addoption("--remote", action="store_true", help="Use remote Selenoid driver")
    parser.addoption("--remote_url", help="Selenoid hub URL", default="http://localhost:4444/wd/hub")
    parser.addoption("--enable_vnc", action="store_true", help="Enable VNC for remote sessions")
    parser.addoption("--enable_video", action="store_true", help="Enable video recording for remote sessions")
    parser.addoption("--browser_version", help="Browser version for remote sessions", default="128.0")  # Новый параметр


@pytest.fixture()
def browser(request):
    driver = None
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    url = request.config.getoption("--url")
    is_remote = request.config.getoption("--remote")
    remote_url = request.config.getoption("--remote_url")
    enable_vnc = request.config.getoption("--enable_vnc")
    enable_video = request.config.getoption("--enable_video")
    browser_version = request.config.getoption("--browser_version")  # Получаем версию браузера

    if is_remote:
        # Настройка для Selenoid
        capabilities = {
            "browserName": "chrome" if browser_name in ["ch", "chrome"] else "firefox",
            "version": browser_version,  # Используем указанную версию или 128.0 по умолчанию
            "enableVNC": enable_vnc,
            "enableVideo": enable_video,
        }

        if browser_name in ["ch", "chrome"]:
            options = CHoptions()
            options.set_capability("selenoid:options", capabilities)
            try:
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
            except Exception as e:
                print(f"Не удалось запустить Chrome {browser_version}, пробуем 127.0: {e}")
                capabilities["version"] = "127.0"
                options = CHoptions()
                options.set_capability("selenoid:options", capabilities)
                driver = webdriver.Remote(
                    command_executor=remote_url,
                    options=options
                )
        elif browser_name in ["ff", "firefox"]:
            options = FFoptions()
            options.set_capability("selenoid:options", capabilities)
            driver = webdriver.Remote(
                command_executor=remote_url,
                options=options
            )
    else:
        # Локальный запуск
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
        return driver.get(url + path.lstrip('/'))

    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.open = open
    driver.open()

    return driver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver is not None:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"screenshot_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    driver.page_source,
                    name="page_source",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"Не удалось сделать скриншот: {e}")