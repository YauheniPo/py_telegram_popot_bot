# -*- coding: utf-8 -*-
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from features.location.map_page import MapPage, what_here_context_item
from util.webdriver_helper import is_visible, wait_for_ajax

logger = logging.getLogger(__name__)


def fetch_map(geo):
    options = Options()
    options.headless = True
    # chrome_options = Options()
    # chrome_options.add_argument("headless")
    # with webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options) as driver:
    with webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options) as driver:
        driver.implicitly_wait(3)
        driver.maximize_window()
        driver.get(geo.geo_map_url)
        map_page = MapPage(driver)
        map_page.right_mouse_click_on_map()
        if is_visible(driver, map_page.context_menu_xpath):
            map_page.select_context_menu_item(what_here_context_item)
        # wait_for_ajax(driver)
        # if is_visible(driver, map_page.ad_close_button_xpath):
        #     map_page.close_ad()
        wait_for_ajax(driver)
        map_page.collapse_searching_list()
        wait_for_ajax(driver)
        driver.save_screenshot(geo.screen_path)
