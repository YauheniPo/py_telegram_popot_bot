import requests
from lxml import html

import config
from features.cinema.cinema import Cinema


def get_site_content(url):
    r = requests.get(url)
    return r.text


def get_tree_movies(site_content):
    tree_html_content = html.fromstring(site_content)
    return tree_html_content.xpath(config.cinema_item_xpath)


def get_movies(tree_movies):
    movies = []
    for movie in tree_movies:
        movie_title = movie.xpath(".//div[@class='event_item__name']//text()")[0]
        movie_date = movie.xpath(".//time//text()")[0]
        movie_ticket_link = movie.xpath(".//div[@class='event_item__buy']/a")[0].get("href")
        movies.append(Cinema(title=movie_title, date=movie_date, ticket_link=config.cinema_url + movie_ticket_link))
    return movies


def get_cinema_data_message(movies):
    return "\n".join(["<a href='{link}'>{title}</a> {date}"
                     .format(link=movie.ticket_link, title=movie.title, date=movie.date) for movie in movies])
