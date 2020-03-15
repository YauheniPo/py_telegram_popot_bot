# -*- coding: utf-8 -*-
from bot_config import browser
from features.location.map_page import MapPage, WHAT_HERE_CONTEXT_ITEM
from util.webdriver_helper import (WebDriverFactory, get_firefox_options,
                                   is_visible, wait_for_ajax)


def fetch_map(geo):
    with WebDriverFactory(browser).get_webdriver_instance(options=get_firefox_options()) as driver:
        driver.get(geo.geo_map_url)
        map_page = MapPage(driver)
        map_page.right_mouse_click_on_map()
        map_page.select_context_menu_item(WHAT_HERE_CONTEXT_ITEM) if is_visible(driver,
                                                                                map_page.CONTEXT_MENU_XPATH) else ...
        wait_for_ajax(driver)
        map_page.collapse_searching_list()
        wait_for_ajax(driver)
        driver.save_screenshot(geo.screen_path)
