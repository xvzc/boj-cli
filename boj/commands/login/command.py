import os
import time

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import boj.core.auth as auth
import boj.core.util as util
import json

from boj.core.console import BojConsole
import chromedriver_autoinstaller
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def execute(args):
    try:
        os.makedirs(util.temp_dir(), exist_ok=True)
        os.makedirs(util.drivers_dir(), exist_ok=True)
    except OSError as e:
        raise e

    driver_path = chromedriver_autoinstaller.install(path=util.drivers_dir())

    options = Options()
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options, service=Service(executable_path=driver_path))
    driver.get(url='https://www.acmicpc.net/login?next=%2F')

    while True:
        if 'acmicpc.net/login' not in driver.current_url:
            break

        try:
            element = driver.find_element(By.NAME, "auto_login")
            if not element.is_selected():
                element.click()
                driver.find_element(By.NAME, "login_user_id").click()
                continue
        except StaleElementReferenceException:
            continue
        except NoSuchElementException:
            break

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'username')))

    username = element.text
    cookie = driver.get_cookie("bojautologin")
    driver.close()

    console = BojConsole()
    if 'value' not in cookie:
        console.print("[red]Login failed")
        exit(1)

    credential = {
        "user": username,
        "token": cookie['value'],
    }

    with console.status("Creating an encryption key...") as status:
        key = auth.create_key()
        time.sleep(0.3)

        status.update("Encrypting the credential...")
        time.sleep(0.3)
        encrypted = auth.encrypt(key, json.dumps(credential))

        status.update("Writing to file...")
        time.sleep(0.3)
        util.write_file(util.key_file_path(), key, "wb")
        util.write_file(util.credential_file_path(), encrypted, "wb")

    console.print("[green]Login succeeded")
