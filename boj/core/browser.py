from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager

from boj.core import constant
from boj.core.error import IllegalStatementError


class RemoteWebDriver:
    pass


def initialize_driver(
    browser: str,
    cache_manager: DriverCacheManager,
):
    if browser == "firefox":
        return webdriver.Firefox(
            service=Service(GeckoDriverManager(cache_manager=cache_manager).install()),
        )
    elif browser == "chrome":
        return webdriver.Chrome(
            service=Service(ChromeDriverManager(cache_manager=cache_manager).install()),
        )
    elif browser == "edge":
        return webdriver.Edge(
            service=Service(ChromeDriverManager(cache_manager=cache_manager).install()),
        )
    else:
        raise IllegalStatementError(f"{browser} is not a valid browser")


class Browser:
    driver: WebDriver
    url: str

    def __init__(self, url: str, browser: str):
        self.url = url
        driver_cache_manager = DriverCacheManager(root_dir=constant.boj_cli_path())

        self.driver = initialize_driver(browser, driver_cache_manager)
        self.driver.maximize_window()

    def open(self):
        self.driver.get(url=self.url)

    def close(self):
        self.driver.close()
