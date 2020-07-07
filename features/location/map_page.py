# -*- coding: utf-8 -*-
from selenium.webdriver import ActionChains

from util.logger import logger

WHAT_HERE_CONTEXT_ITEM = "Что здесь?"


class MapPage:
    SEARCH_DATA_COLLAPSE_BUTTON_XPATH = "//*[@class='sidebar-toggle-button']//span"
    AD_CLOSE_BUTTON_XPATH = "//*[@class='_noprint']//*[@fill]"
    MAP_CONTAINER_XPATH = "//div[@class='map-container']"
    CONTEXT_MENU_XPATH = "//div[@class='context-menu']"
    CONTEXT_MENU_XPATH_ITEM = CONTEXT_MENU_XPATH + "/div[text()='{}']"

    def __init__(self, driver):
        self.web_driver = driver
        logger().info("Driver init.")

    def collapse_searching_list(self):
        self.web_driver.find_element_by_xpath(
            self.SEARCH_DATA_COLLAPSE_BUTTON_XPATH).click()

    def close_ad(self):
        self.web_driver.find_element_by_xpath(
            self.AD_CLOSE_BUTTON_XPATH).click()

    def right_mouse_click_on_map(self):
        map = self.web_driver.find_element_by_xpath(self.MAP_CONTAINER_XPATH)
        actionChains = ActionChains(self.web_driver)
        actionChains.context_click(map).perform()

    def select_context_menu_item(self, item_name):
        self.web_driver.find_element_by_xpath(
            self.CONTEXT_MENU_XPATH_ITEM.format(item_name)).click()
