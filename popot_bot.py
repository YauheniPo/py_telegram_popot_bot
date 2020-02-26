# -*- coding: utf-8 -*-
import time

import telebot
from telebot import types
from telegram import ParseMode

from base.bot_script import send_currency_rate, get_message_keyboard, send_instagram_media, send_map_location
from bot_constants import *
from db.db_connection import users_table, users
from features.cinema.cinema_site_parser import *
from features.currency.currency_api import *
from features.currency.currency_graph_generator import fetch_currency_graph
from features.football.football_site_parser import *
from features.instagram.insta_loader import *
from util.util_parsing import is_match_by_regexp
from util.util_request import get_site_request_content

TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN')
TELEGRAM_BOT_NAME = os.environ.get('BOT_NAME')
bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN, threaded=False)


def get_db_user(user_id):
    db_users = users_table.search(users.id == user_id)
    return db_users[0] if db_users else []


from base.user import User


def get_user(user_id):
    user = User(user_db=get_db_user(user_id=user_id))
    logger().info("***** {} *****".format(user.__dict__))
    return user


def fetch_user(chat):
    user = get_db_user(chat.id)
    if not user:
        users_table.insert({'id': chat.id, 'username': chat.username,
                            'first_name': chat.first_name, 'last_name': chat.last_name})
    return get_user(user_id=chat.id)


@bot.message_handler(regexp='^\{start}'.format(start=BASE_CMD_START))
def start(message):
    user = fetch_user(chat=message.chat)

    bot.send_message(chat_id=user.user_id,
                     text=MSG_START_CMD_BASE.format(start=BASE_CMD_START,
                                                    currency=BASE_CMD_CURRENCY,
                                                    cinema=BASE_CMD_CINEMA,
                                                    football=BASE_CMD_FOOTBALL,
                                                    instagram=BASE_CMD_INSTAGRAM,
                                                    geo=BASE_CMD_GEO))


@bot.message_handler(regexp='^\{command}'.format(command=BASE_CMD_CURRENCY))
@bot.callback_query_handler(func=lambda call: call.data in currency_ids)
def currency(message):
    if type(message) == Message:
        chat = message.chat
        actual_currency = bot_config.currency_dollar_id
    else:
        chat = message.message.chat
        actual_currency = message.data

    user = get_user(user_id=chat.id)

    send_currency_rate(bot, user, actual_currency)


@bot.message_handler(regexp='^\{cinema}'.format(cinema=BASE_CMD_CINEMA))
def cinema(message):
    user = get_user(user_id=message.chat.id)

    movies = get_movies(get_site_request_content(bot_config.cinema_url + bot_config.cinema_url_path_today))

    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     reply_markup=get_message_keyboard(button_cinema_soon),
                     parse_mode=ParseMode.HTML)


@bot.message_handler(regexp='^\{football}'.format(football=BASE_CMD_FOOTBALL))
def football(message):
    user = get_user(user_id=message.chat.id)

    bot.send_message(chat_id=user.user_id,
                     text=MSG_FOOTBALL_BASE_CMD,
                     reply_markup=get_message_keyboard(*[{k: v} for (k, v) in buttons_football_leagues.items()]))


@bot.message_handler(regexp='^\{instagram}'.format(instagram=BASE_CMD_INSTAGRAM))
def instagram(message):
    user = get_user(user_id=message.chat.id)

    bot.send_message(chat_id=user.user_id,
                     text=MSG_INSTAGRAM_BOT)


@bot.message_handler(regexp='^\{geo}'.format(geo=BASE_CMD_GEO))
def geo(message):
    user = get_user(user_id=message.chat.id)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(user.user_id, "Hello! Click on the button and give me your location.", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    user = get_user(user_id=message.chat.id)

    if message.location is not None:
        send_map_location(bot, user, message)


@bot.message_handler(
    func=lambda message: message.text is not None and is_match_by_regexp(message.text, instagram_link_regexp))
def send_instagram_post_content(message):
    user = get_user(user_id=message.chat.id)

    user_message = message.text
    logger().info("User message: '{}'".format(user_message))

    send_instagram_media(bot, message, user)


@bot.message_handler(content_types=['text', 'document'], func=lambda message: True)
def echo_all(message):
    user = get_user(user_id=message.chat.id)

    user_message = message.text
    logger().info("User message: '{}'".format(user_message))


@bot.callback_query_handler(func=lambda call: call.data == currency_graph)
def send_currency_graph(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    actual_currency = list(
        set(currency_ids) - set([currency_data['callback_data']
                                 for currency_data in call.message.json['reply_markup']['inline_keyboard'][1]]))[0]

    currency_data_bot = fetch_currency_list(get_currency_response_json(actual_currency))
    fetch_currency_graph(currency_data_bot)

    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[actual_currency]

    bot.send_photo(chat_id=user.user_id,
                   reply_markup=get_message_keyboard(actual_buttons_currency_selection),
                   photo=open(currency_graph_path, 'rb'))


@bot.callback_query_handler(func=lambda call: call.data == cinema_soon)
def send_cinema_soon(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    movies = get_movies(get_site_request_content(url=bot_config.cinema_url + bot_config.cinema_url_path_soon,
                                                 params=cinema_soon_params))
    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     parse_mode=ParseMode.HTML)


@bot.callback_query_handler(func=lambda call: call.data in football_leagues_cmd)
def send_football_calendar(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    matches = get_matches(get_site_request_content(
        url=bot_config.football_url + call.data + bot_config.football_url_path_calendar))

    actual_buttons_football = dict(buttons_football_leagues)
    football_message_title = actual_buttons_football.pop(call.data)

    bot.send_message(chat_id=user.user_id,
                     text="<b>{}</b>\n\n".format(football_message_title) + get_football_data_message(matches),
                     reply_markup=get_message_keyboard(actual_buttons_football),
                     parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    for i in range(0, 5):
        time.sleep(0.1)
        try:
            bot.infinity_polling()
        except Exception as e:
            logger().error(e)

# bot.register_next_step_handler(message, func) #следующий шаг – функция func(message)

# base_buttons = ReplyKeyboardMarkup(resize_keyboard=True)  # под клавиатурой
# base_buttons.add(KeyboardButton(base_cmd_currency), KeyboardButton(base_cmd_start))
