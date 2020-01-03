# -*- coding: utf-8 -*-
import re

import telebot
from telebot import types
from telegram import ParseMode

from config import *
from features.cinema.cinema_site_parsing import *
from features.currency.currency_api import *
from features.currency.graph import fetch_currency_graph
from features.football.football_site_parsing import *
from features.instagram.insta_loader import *
from msg_context import *
from user import User
from util.util_date import currency_msg_date_format
from util.util_parsing import is_match_by_regexp
from util.util_request import get_site_content

bot = telebot.TeleBot(token=os.environ.get('bot_token'))

users = dict()


def get_user(user_id=None, message=None):
    if bool(os.environ.get('demo')):
        if user_id is None:
            return User(message=message)
        return User(user_id=user_id)

    if user_id is None:
        return users[message.from_user.id]
    return users[user_id]


base_cmd_start = '/start'
base_cmd_currency = '/currency'
base_cmd_cinema = '/cinema'
base_cmd_football = '/football'
base_cmd_instagram = '/instagram'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    format=u'%(asctime)s %(levelname)-8s %(name)-45s %(message)s',
                    level=logging.INFO)


def get_message_keyboard(key_dict):
    message_keyboard = types.InlineKeyboardMarkup()
    for key in key_dict:
        button = types.InlineKeyboardButton(text=key, callback_data=key_dict[key])
        message_keyboard.add(button)
    logger.info("Get message keyboard: {}".format(key_dict))
    return message_keyboard


@bot.message_handler(regexp='^\{start}'.format(start=base_cmd_start))
def start(message):
    users[message.from_user.id] = User(message=message)

    bot.send_message(chat_id=get_user(message=message).user_id,
                     text=start_base_cmd_text.format(start=base_cmd_start,
                                                     currency=base_cmd_currency,
                                                     cinema=base_cmd_cinema,
                                                     football=base_cmd_football,
                                                     instagram=base_cmd_instagram))


@bot.message_handler(regexp='^\{command}'.format(command=base_cmd_currency))
def currency(message):
    user = get_user(message=message)

    currency_list = fetch_currency_list(get_currency_response_json())

    currency_response_past_days = get_currency_data_message(currency_list[-10:-1], currency_msg_date_format)
    currency_response_current_day = get_currency_data_message([currency_list[-1]], currency_msg_date_format)

    bot.send_message(chat_id=user.user_id,
                     text=currency_bot_text.format(
                         currency_past_days=currency_response_past_days,
                         currency_current_day=currency_response_current_day),
                     reply_markup=get_message_keyboard(button_currency_graph),
                     parse_mode=ParseMode.HTML)


@bot.message_handler(regexp='^\{cinema}'.format(cinema=base_cmd_cinema))
def cinema(message):
    user = get_user(message=message)

    movies = get_movies(get_site_content(config.cinema_url + config.cinema_url_path_today))

    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     reply_markup=get_message_keyboard(button_cinema_soon),
                     parse_mode=ParseMode.HTML)


@bot.message_handler(regexp='^\{football}'.format(football=base_cmd_football))
def football(message):
    user = get_user(message=message)

    bot.send_message(chat_id=user.user_id,
                     text=football_base_cmd_text,
                     reply_markup=get_message_keyboard(buttons_football))


@bot.message_handler(regexp='^\{instagram}'.format(instagram=base_cmd_instagram))
def instagram(message):
    user = get_user(message=message)

    bot.send_message(chat_id=user.user_id,
                     text=instagram_bot_text)


@bot.message_handler(content_types=['text', 'document'], func=lambda message: True)
def echo_all(message):
    user = get_user(message=message)

    if is_match_by_regexp(message.text, instagram_link_regexp):
        insta_post = get_insta_post_data(get_site_content(re.sub('.*w\.', '', message.text, 1)))

        post_description = insta_post.warning
        if post_description is None:
            fetch_insta_post_image(insta_post)

            bot.send_photo(chat_id=user.user_id,
                           photo=open(insta_post.image_path, 'rb'))

            post_description = "<b>Post description</b>\n\n" + insta_post.post_description

        bot.send_message(chat_id=user.user_id,
                         text=post_description,
                         parse_mode=ParseMode.HTML)
    else:
        bot.send_message(chat_id=user.user_id,
                         text=message.text)
    # bot.register_next_step_handler(message, func) #следующий шаг – функция func(message)

    # base_buttons = ReplyKeyboardMarkup(resize_keyboard=True)  # под клавиатурой
    # base_buttons.add(KeyboardButton(base_cmd_currency), KeyboardButton(base_cmd_start))


@bot.callback_query_handler(func=lambda call: True)  # обработчик кнопок
def callback_worker(call):
    logger.info("Button '{}'".format(call.data))
    user = get_user(call.from_user.id)

    if call.data == currency_graph:
        currency_data_bot = fetch_currency_list(get_currency_response_json())
        fetch_currency_graph(currency_data_bot)
        bot.send_photo(chat_id=user.user_id,
                       photo=open(currency_graph_path, 'rb'))

    elif call.data == cinema_soon:
        movies = get_movies(get_site_content(url=config.cinema_url + config.cinema_url_path_soon,
                                             params=cinema_soon_params))
        bot.send_message(chat_id=user.user_id,
                         text=get_cinema_data_message(movies),
                         parse_mode=ParseMode.HTML)

    elif call.data in buttons_football.values():
        matches = get_matches(get_site_content(url=config.football_url + call.data + config.football_url_path_calendar))
        football_message_title = [key for key, value in buttons_football.items() if value == call.data][0]

        actual_buttons_football = dict(buttons_football)
        del actual_buttons_football[football_message_title]

        bot.send_message(chat_id=user.user_id,
                         text="<b>{}</b>\n\n".format(football_message_title) + get_football_data_message(matches),
                         reply_markup=get_message_keyboard(actual_buttons_football),
                         parse_mode=ParseMode.HTML)


bot.polling(none_stop=True)
