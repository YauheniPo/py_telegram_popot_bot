# -*- coding: utf-8 -*-
import datetime
import os

from selenium.common.exceptions import NoSuchElementException

from bot_config import instagram_save_content_service
from util.logger import logger
from util.webdriver_helper import WebDriverFactory, wait_for_ajax, wait_visibility, take_screenshot, FIREFOX


def fetch_insta_post_data(insta_post_model):
    insta_media_description_xpath = "//div[@class='row title']"
    searching_result = "//div[@id='sf_result']/div[contains(@class, 'result')]"
    results_for_download = f"{searching_result}//a[@download]"

    with WebDriverFactory(FIREFOX).get_webdriver_instance() as driver:
        try:
            driver.get(
                instagram_save_content_service +
                insta_post_model.post_url)
            wait_visibility(True, driver, searching_result)
            wait_for_ajax(driver)
            insta_post_items = driver.find_elements_by_xpath(
                results_for_download)
            post_media_urls = [media.get_attribute(
                "href") for media in insta_post_items]
            insta_post_model.media_urls = post_media_urls
            insta_post_description = driver.find_element_by_xpath(
                insta_media_description_xpath).text
            insta_post_model.post_description = insta_post_description
        except NoSuchElementException as ex:
            take_screenshot(
                driver,
                os.path.join(
                    "screenshot",
                    f"{datetime.datetime.now().microsecond}.jpg"))
            raise ex

    logger().info(("--Instagram instance-- '{}'".format(insta_post_model.__dict__)).encode("utf-8"))
