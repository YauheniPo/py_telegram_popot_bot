# -*- coding: utf-8 -*-
import lxml.html.clean
from lxml import html
from lxml.html import HtmlElement

from base.constants import MSG_CINEMA_BOT
from features.cinema.cinema import Cinema
from util.logger import logger

MOVIES_POSTER = "Киноафиша"

DIV_TAG = 'div'
UL_TAG = 'ul'

MOVIES_TITLE_BLOCK = "//div[@class='title_block']"
MOVIE_TICKETS_BLOCK = f"//div[@id='events-block']/*[contains(@class, 'b-lists')][./li | .{MOVIES_TITLE_BLOCK}]"
MOVIE_TITLE_XPATH = "//a[@class='name']"
MOVIE_MEDIA_XPATH = "//a[@class='media']"
MOVIE_INFO_XPATH = "//div[@class='txt']//p"
MOVIE_TICKET_XPATH = ".//a[@class='media']"

XPATH_GET_TEXT = ".{xpath}//text()"


def fetch_movies(movie_block: HtmlElement):
    movies = []

    for movie in movie_block.getchildren():
        movie_title = movie.xpath(
            XPATH_GET_TEXT.format(
                xpath=MOVIE_TITLE_XPATH))[0]
        movie_media = str(
            ''.join(
                movie.xpath(
                    XPATH_GET_TEXT.format(
                        xpath=MOVIE_MEDIA_XPATH)))).strip()
        movie_info_list = movie.xpath(
            XPATH_GET_TEXT.format(
                xpath=MOVIE_INFO_XPATH))
        movie_info = movie_info_list[0] if movie_info_list else ""
        movie_ticket_link = movie.xpath(MOVIE_TICKET_XPATH)[0].get("href")
        movies.append(
            Cinema(
                title=movie_title,
                media=movie_media,
                info=movie_info,
                ticket_link=movie_ticket_link
            )
        )

    return movies


def get_movies(site_content):
    logger().info("Get movies")

    movies_section: str = MOVIES_POSTER
    movies: dict[str: list] = {}

    cleaner = html.clean.Cleaner(style=True)
    html_site_elements_content = cleaner.clean_html(html.fromstring(site_content))

    for movie in html_site_elements_content.xpath(MOVIE_TICKETS_BLOCK):  # type: HtmlElement
        movie_block_tag = movie.tag
        if movie_block_tag == DIV_TAG:
            movies_section = movie.xpath(XPATH_GET_TEXT.format(xpath=MOVIES_TITLE_BLOCK))[0].strip()
            continue
        movies_poster = [] if movies.get(movies_section) is None else movies[movies_section]
        movies[movies_section] = movies_poster + fetch_movies(movie)

    return movies


def get_cinema_data_message(movies: dict):
    cinema_data_message = ""
    for section, movies in movies.items():
        cinema_data_message = cinema_data_message + """

<b>{}</b>
{}""".format(section, "\n".join(
            [
                MSG_CINEMA_BOT.format(
                    link=movie.ticket_link,
                    title=movie.title,
                    info=movie.info,
                    media=movie.media) for movie in movies
            ]
        ))
    return cinema_data_message
