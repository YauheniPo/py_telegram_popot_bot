from telegram import ParseMode

import bot_config
from base.bot.bot import bot
from features.cinema.cinema_site_parser import get_movies, get_cinema_data_message
from util.bot_helper import get_message_keyboard
from util.util_request import get_site_request_content


def send_cinema_list(user):
    movies = get_movies(
        get_site_request_content(
            bot_config.cinema_url +
            bot_config.cinema_url_path_today))

    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     reply_markup=get_message_keyboard(bot_config.button_cinema_soon),
                     parse_mode=ParseMode.HTML)


def send_cinema_soon_list(user):
    movies = get_movies(
        get_site_request_content(
            url=bot_config.cinema_url + bot_config.cinema_url_path_soon,
            params=bot_config.cinema_soon_params))
    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     parse_mode=ParseMode.HTML)
