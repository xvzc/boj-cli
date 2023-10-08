from abc import *

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import ChromiumDriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager

from boj.core.config import Config
from boj.core import constant


class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, args, config: Config):
        """Implement this method"""


class Page:
    html: str


class Api:
    url: str

    @abstractmethod
    def request(self):
        """Implement this method"""


class Browser:
    driver: ChromiumDriver
    url: str

    def __init__(self, url):
        self.url = url
        options = Options()
        options.add_argument("start-maximized")
        driver_cache_manager = DriverCacheManager(root_dir=constant.boj_dir_path())

        self.driver = webdriver.Chrome(
            options=options,
            service=Service(
                ChromeDriverManager(cache_manager=driver_cache_manager).install()
            ),
        )

    def open(self):
        self.driver.get(url=self.url)

    def close(self):
        self.driver.close()
