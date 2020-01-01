import logging

from lxml import html

import config
from features.cinema.cinema import Cinema
from msg_context import cinema_bot_text

cinema_soon_params = {'utm_source': config.cinema_url, 'utm_medium': 'films', 'utm_campaign': 'premiere_block'}

logger = logging.getLogger(__name__)


def get_tree_movies(site_content):
    tree_html_content = html.fromstring(site_content)
    return tree_html_content.xpath("//div[contains(@class, 'events')]/ul//li")


def get_movies(tree_movies):
    logger.info("Get movies")

    movies = []
    for movie in tree_movies:
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
