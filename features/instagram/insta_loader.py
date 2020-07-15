# -*- coding: utf-8 -*-
from bot_config import *
from util.util_request import *
from util.webdriver_helper import WebDriverFactory, wait_for_ajax, wait_visibility


def fetch_insta_post_data(insta_post_model):
    insta_media_description_xpath = "//div[@class='row title']"
    results_for_download = "//div[@id='sf_result']//a[@download]"

    with WebDriverFactory(browser).get_webdriver_instance() as driver:
        driver.get(instagram_save_content_service + insta_post_model.post_url)
        wait_visibility(True, driver, results_for_download)
        wait_for_ajax(driver)
        insta_post_items = driver.find_elements_by_xpath(results_for_download)
        post_media_urls = [media.get_attribute(
            "href") for media in insta_post_items]
        insta_post_model.media_urls = post_media_urls
        insta_post_description = driver.find_element_by_xpath(
            insta_media_description_xpath).text
        insta_post_model.post_description = insta_post_description

    logger().info(("--Instagram instance-- '{}'".format(insta_post_model.__dict__)).encode("utf-8"))
