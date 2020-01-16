# -*- coding: utf-8 -*-
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from features.location.map_page import MapPage

logger = logging.getLogger(__name__)


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        logger.error(e)


def fetch_map(geo):
    chrome_options = Options()
    # chrome_options.add_argument("headless")
    with webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options) as driver:
        driver.implicitly_wait(10)
        driver.maximize_window()
        driver.get(geo.geo_map_url)
        map_page = MapPage(driver)
        # map_page.right_mouse_click_on_map()
        # map_page.select_context_menu_item()
        map_page.collapse_searching_list()
        wait_for_ajax(driver)
        driver.save_screenshot(geo.screen_path)
