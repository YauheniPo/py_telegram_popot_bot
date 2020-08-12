# -*- coding: utf-8 -*-
import os

import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from util.logger import logger

FIREFOX = 'FIREFOX'
CHROME = 'CHROME'


def get_firefox_options():
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.add_argument("--headless")
    return options


def get_chrome_options():
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    return chrome_options


class WebDriverFactory:

    def __init__(self, browser: str):
        self.browser = browser.upper()
        self.driver = None

    def get_webdriver_instance(self, timeout=3, cookies=None):
        logger().info(
            "Initialization of {browser}.".format(
                browser=self.browser))

        if self.browser == 'FIREFOX':
            executable_path = GeckoDriverManager().install()
            self.driver = webdriver.Firefox(
                executable_path=executable_path,
                options=get_firefox_options())
        if self.browser == 'CHROME':
            executable_path = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(
                executable_path=executable_path,
                options=get_chrome_options())

        logger().info(f"Created instance of '{self.browser}' browser.")

        self.driver.implicitly_wait(timeout)
        self.driver.maximize_window()
        if cookies is None:
            cookies = {}
        for cookies in cookies:
            self.driver.add_cookie(cookie_dict=cookies)
        return self.driver


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 30)
    try:
        wait.until(lambda driver: driver.execute_script(
            'return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script(
            'return document.readyState') == 'complete')
    except Exception as e:
        logger().error(e)


def wait_visibility(
        is_visible: bool,
        driver,
        locator: str,
        timeout=60) -> bool:
    action = EC.visibility_of_element_located(
        (By.XPATH, locator))
    if not is_visible:
        action = EC.invisibility_of_element_located(
            (By.XPATH, locator))
    try:
        ui.WebDriverWait(
            driver, timeout).until(action)
        return True
    except TimeoutException:
        return False


def take_screenshot(driver, screenshot):
    screen_folder = os.path.dirname(screenshot)
    if not os.path.exists(screen_folder):
        os.makedirs(screen_folder)
    driver.save_screenshot(screenshot)
