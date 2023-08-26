from abc import *

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from boj.core import property

from selenium.webdriver.chrome.webdriver import WebDriver
import chromedriver_autoinstaller


class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, args):
        """Implement this method"""


class BojError(BaseException):
    def __init__(self, msg):
        super().__init__(msg)


class Page:
    html: str


class Api:
    url: str

    @abstractmethod
    def request(self):
        """Implement this method"""


class Browser:
    driver: WebDriver
    url: str

    def __init__(self, url):
        self.url = url
        options = Options()
        options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(options=options, service=Service())

    def open(self):
        self.driver.get(url=self.url)

    def close(self):
        self.driver.close()
