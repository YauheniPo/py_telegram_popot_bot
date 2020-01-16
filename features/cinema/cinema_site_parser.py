# -*- coding: utf-8 -*-
import logging

from features.cinema.cinema import Cinema
from base.msg_context import cinema_bot_text
from util.util_parsing import get_tree_html_content

logger = logging.getLogger(__name__)


def get_movies(site_content):
    logger.info("Get movies")

    movies_tree_xpath = "//div[contains(@class, 'events')]/ul//li"
    movie_title_xpath = ".//a[@class='name']"
    movie_media_xpath = ".//a[@class='media']"
    movie_info_xpath = ".//div[@class='txt']//p"
    movie_ticket_xpath = ".//a[@class='media']"

    movies = []

    xpath_get_text = "{xpath}//text()"
    for movie in get_tree_html_content(site_content).xpath(movies_tree_xpath):
        movie_title = movie.xpath(xpath_get_text.format(xpath=movie_title_xpath))[0]
        movie_media = str(''.join(movie.xpath(xpath_get_text.format(xpath=movie_media_xpath)))).strip()
        movie_info_list = movie.xpath(xpath_get_text.format(xpath=movie_info_xpath))
        movie_info = movie_info_list[0] if movie_info_list else ""
        movie_ticket_link = movie.xpath(movie_ticket_xpath)[0].get("href")
        movies.append(Cinema(title=movie_title, media=movie_media, info=movie_info, ticket_link=movie_ticket_link))
    return movies


def get_cinema_data_message(movies):
    return "\n".join(
        [cinema_bot_text.format(link=movie.ticket_link, title=movie.title, info=movie.info, media=movie.media)
         for movie in movies])
