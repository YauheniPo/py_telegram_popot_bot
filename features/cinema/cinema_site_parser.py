# -*- coding: utf-8 -*-
import logging

from features.cinema.cinema import Cinema
from bot_constants import MSG_CINEMA_BOT
from util.util_parsing import get_tree_html_content

logger = logging.getLogger(__name__)


def get_movies(site_content):
    logger.info("Get movies")

    MOVIES_TREE_XPATH = "//div[contains(@class, 'events')]/ul//li"
    MOVIE_TITLE_XPATH = ".//a[@class='name']"
    MOVIE_MEDIA_XPATH = ".//a[@class='media']"
    MOVIE_INFO_XPATH = ".//div[@class='txt']//p"
    MOVIE_TICKET_XPATH = ".//a[@class='media']"

    movies = []

    xpath_get_text = "{xpath}//text()"
    for movie in get_tree_html_content(site_content).xpath(MOVIES_TREE_XPATH):
        movie_title = movie.xpath(xpath_get_text.format(xpath=MOVIE_TITLE_XPATH))[0]
        movie_media = str(''.join(movie.xpath(xpath_get_text.format(xpath=MOVIE_MEDIA_XPATH)))).strip()
        movie_info_list = movie.xpath(xpath_get_text.format(xpath=MOVIE_INFO_XPATH))
        movie_info = movie_info_list[0] if movie_info_list else ""
        movie_ticket_link = movie.xpath(MOVIE_TICKET_XPATH)[0].get("href")
        movies.append(Cinema(title=movie_title, media=movie_media, info=movie_info, ticket_link=movie_ticket_link))
    return movies


def get_cinema_data_message(movies):
    return "\n".join(
        [MSG_CINEMA_BOT.format(link=movie.ticket_link, title=movie.title, info=movie.info, media=movie.media)
         for movie in movies])
