from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver

from boj.core import constant
from boj.core.error import IllegalStatementError, FatalError


class RemoteWebDriver:
    pass

def initialize_driver(
    browser: str,
):
    if browser == "firefox":
        return webdriver.Firefox()
    elif browser == "chrome":
        return webdriver.Chrome()
    elif browser == "edge":
        return webdriver.Edge()
    else:
        raise FatalError(f"{browser} is not a valid browser")


class Browser:
    driver: WebDriver
    url: str

    def __init__(self, url: str, browser: str):
        self.url = url

        self.driver = initialize_driver(browser)
        self.driver.maximize_window()

    def open(self):
        self.driver.get(url=self.url)

    def close(self):
        self.driver.close()
