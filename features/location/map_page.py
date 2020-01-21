# -*- coding: utf-8 -*-
import logging

from selenium.webdriver import ActionChains

logger = logging.getLogger(__name__)

what_here_context_item = "Что здесь?"


class MapPage:
    search_data_collapse_button_xpath = "//*[@class='sidebar-toggle-button']//span"
    ad_close_button_xpath = "//*[@class='_noprint']//*[@fill]"
    map_container_xpath = "//div[@class='map-container']"
    context_menu_xpath = "//div[@class='context-menu']"
    context_menu_xpath_item = context_menu_xpath + "/div[text()='{}']"

    def __init__(self, driver):
        self.web_driver = driver
        logger.info("Driver init.")

    def collapse_searching_list(self):
        self.web_driver.find_element_by_xpath(self.search_data_collapse_button_xpath).click()

    def close_ad(self):
        self.web_driver.find_element_by_xpath(self.ad_close_button_xpath).click()

    def right_mouse_click_on_map(self):
        map = self.web_driver.find_element_by_xpath(self.map_container_xpath)
        actionChains = ActionChains(self.web_driver)
        actionChains.context_click(map).perform()

    def select_context_menu_item(self, item_name):
        self.web_driver.find_element_by_xpath(self.context_menu_xpath_item.format(item_name)).click()
