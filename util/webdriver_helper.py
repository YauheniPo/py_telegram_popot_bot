# -*- coding: utf-8 -*-
import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from logger import logger


class WebDriverFactory():

    def __init__(self, browser: str):
        self.browser = browser.upper()
        self.driver = None

    def get_webdriver_instance(self, options=None, timeout=3):
        logger().info(
            "Initialization of {browser}.".format(
                browser=self.browser))
        if self.browser == 'FIREFOX':
            self.driver = webdriver.Firefox(
                executable_path=GeckoDriverManager().install(), options=options)
        if self.browser == 'CHROME':
            self.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=options)
        self.driver.implicitly_wait(timeout)
        self.driver.maximize_window()
        return self.driver


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script(
            'return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script(
            'return document.readyState') == 'complete')
    except Exception as e:
        logger().error(e)


def is_visible(driver, locator: str, timeout=3) -> bool:
    try:
        ui.WebDriverWait(
            driver, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, locator)))
        return True
    except TimeoutException:
        return False


def get_firefox_options():
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.headless = True
    return options


def get_chrome_options():
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    return options
