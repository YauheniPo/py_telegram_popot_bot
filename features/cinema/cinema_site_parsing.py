# -*- coding: utf-8 -*-
import logging

import config
from features.cinema.cinema import Cinema
from msg_context import cinema_bot_text
from util.util_parsing import get_tree_html_content

cinema_soon_params = {'utm_source': config.cinema_url, 'utm_medium': 'films', 'utm_campaign': 'premiere_block'}

logger = logging.getLogger(__name__)


def get_movies(site_content):
    logger.info("Get movies")

    movies = []
    for movie in get_tree_html_content(site_content).xpath("//div[contains(@class, 'events')]/ul//li"):
        movie_title = movie.xpath(".//a[@class='name']//text()")[0]
        movie_media = str(''.join(movie.xpath(".//a[@class='media']//text()"))).strip()
        tree_movie_info = movie.xpath(".//div[@class='txt']//p//text()")
        movie_info = tree_movie_info[0] if len(tree_movie_info) > 0 else ""
        movie_ticket_link = movie.xpath(".//a[@class='media']")[0].get("href")
        movies.append(Cinema(title=movie_title, media=movie_media, info=movie_info, ticket_link=movie_ticket_link))
    return movies


def get_cinema_data_message(movies):
    return "\n".join(
        [cinema_bot_text.format(link=movie.ticket_link, title=movie.title, info=movie.info, media=movie.media)
         for movie in movies])
