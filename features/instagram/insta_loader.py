# -*- coding: utf-8 -*-
from bot_config import *
from util.util_request import *
from util.webdriver_helper import get_chrome_options, WebDriverFactory, wait_for_ajax, wait_visibility


def fetch_insta_post_data(insta_post_model):
    results_xpath = "//div[@class='result-box video']"
    insta_media_description_xpath = "//div[@class='row title']"
    downloader_spinner = "//div[contains(@class, 'downloader-2-part2')]"

    with WebDriverFactory(browser).get_webdriver_instance(options=get_chrome_options()) as driver:
        driver.get(instagram_save_content_service + insta_post_model.post_url)
        wait_for_ajax(driver)
        wait_visibility(False, driver, downloader_spinner)
        insta_post_items = driver.find_elements_by_xpath(results_xpath)
        post_media_urls = [media.find_element_by_xpath(".//img").get_attribute("src") for media in insta_post_items]
        insta_post_model.media_urls = post_media_urls
        insta_post_description = driver.find_element_by_xpath(insta_media_description_xpath).text
        insta_post_model.post_description = insta_post_description

    logger().info(("--Instagram instance-- '{}'".format(insta_post_model.__dict__)).encode("utf-8"))
