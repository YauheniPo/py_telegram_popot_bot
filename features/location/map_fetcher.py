# -*- coding: utf-8 -*-
from features.location.map_page import WHAT_HERE_CONTEXT_ITEM, MapPage
from util.webdriver_helper import (
    WebDriverFactory,
    wait_visibility,
    wait_for_ajax, take_screenshot, FIREFOX)


def fetch_map(geo):
    with WebDriverFactory(FIREFOX).get_webdriver_instance() as driver:
        driver.get(geo.geo_map_url)
        map_page = MapPage(driver)
        map_page.right_mouse_click_on_map()
        map_page.select_context_menu_item(WHAT_HERE_CONTEXT_ITEM) if wait_visibility(
            True, driver, map_page.CONTEXT_MENU_XPATH) else ...
        wait_for_ajax(driver)
        map_page.collapse_searching_list()
        wait_for_ajax(driver)
        take_screenshot(driver, geo.screen_path)
