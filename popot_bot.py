# -*- coding: utf-8 -*-
from telebot import types

from base.bot.bot import bot
from base.bot.bot_step import start_step, catch_bot_handler_error
from base.constants import *
from base.models.user import fetch_user, get_user
from db.db_connection import get_db_data, insert_analytics, insert_currency_alarm
from features.cinema.bot_step import send_cinema_list, send_cinema_soon_list
from features.currency.bot_step import send_currency_rate, send_msg_alarm_currency, \
    set_currency_alarm_rate_and_get_new_rate, send_currency_graph
from features.currency.currency_api import *
from features.football.bot_step import send_football_calendar
from features.instagram.bot_step import send_to_user_insta_post_media_content
from features.instagram.insta_loader import *
from features.instagram.insta_post import InstaPost
from features.location.bot_step import send_map_location
from features.virus.bot_step import sent_virus_data
from util.bot_helper import get_message_keyboard
from util.util_data import is_match_by_regexp

__author__ = "Yauheni Papovich"
__email__ = "ip.popovich.1990@gmail.com"

__all__ = [
    'alarm_currency',
    'cinema',
    'currency',
    'db_log',
    'echo_all',
    'football_start',
    'geo_start',
    'instagram_start',
    'location',
    'cinema_soon',
    'currency_graph',
    'football_calendar',
    'instagram_post_content',
    'start',
    'update_currency_alarm_rate',
    'virus'
]


@bot.message_handler(regexp=r'^\{start}'.format(start=BASE_CMD_START))
@catch_bot_handler_error
def start(message):
    user = fetch_user(chat=message.chat)

    start_step(user)
    insert_analytics(user, message.text)


@bot.message_handler(regexp=r'^\{command}'.format(command=BASE_CMD_CURRENCY))
@bot.callback_query_handler(func=lambda call: call.data in currency_ids)
@catch_bot_handler_error
def currency(message):
    user = get_user(message=message)

    actual_currency = getattr(message, 'data', bot_config.currency_dollar_id)
    send_currency_rate(user, actual_currency)
    insert_analytics(user, message.text)


@bot.message_handler(regexp=r'^\{log}'.format(log=DB_LOG_CMD))
@catch_bot_handler_error
def db_log(message):
    user = get_user(user_id=message.chat.id)

    bot.send_message(user.user_id, str(get_db_data()))
    insert_analytics(user, message.text)


@bot.callback_query_handler(func=lambda call: call.data in currency_alarm)
@catch_bot_handler_error
def alarm_currency(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    today_currency_rate, around_today_currency_rate = get_today_currency_rate()
    send_msg_alarm_currency(user, today_currency_rate, around_today_currency_rate)


@bot.callback_query_handler(
    func=lambda call: call.data is not None and is_match_by_regexp(
        call.data, currency_alarm_rate_button_regexp))
@catch_bot_handler_error
def update_currency_alarm_rate(call):
    user = get_user(user_id=call.from_user.id)

    call_message = call.message.text.strip()
    new_currency_alarm_rate = set_currency_alarm_rate_and_get_new_rate(call_message)
    insert_currency_alarm(user, new_currency_alarm_rate)


@bot.message_handler(regexp=r'^\{cinema}'.format(cinema=BASE_CMD_CINEMA))
@catch_bot_handler_error
def cinema(message):
    user = get_user(user_id=message.chat.id)

    send_cinema_list(user)
    insert_analytics(user, message.text)


@bot.message_handler(regexp=r'^\{football}'.format(football=BASE_CMD_FOOTBALL))
@catch_bot_handler_error
def football_start(message):
    user = get_user(user_id=message.chat.id)

    bot.send_message(chat_id=user.user_id,
                     text=MSG_FOOTBALL_BASE_CMD,
                     reply_markup=get_message_keyboard(*[{k: v} for (k,
                                                                     v) in buttons_football_leagues.items()]))
    insert_analytics(user, message.text)


@bot.message_handler(
    regexp=r'^\{instagram}'.format(
        instagram=BASE_CMD_INSTAGRAM))
@catch_bot_handler_error
def instagram_start(message):
    user = get_user(user_id=message.chat.id)

    bot.send_message(user.user_id, MSG_INSTAGRAM_BOT)
    insert_analytics(user, message.text)


@bot.message_handler(
    func=lambda message: message.text is not None and is_match_by_regexp(
        message.text, instagram_link_regexp))
@catch_bot_handler_error
def instagram_post_content(message):
    user = get_user(user_id=message.chat.id)

    send_to_user_insta_post_media_content(InstaPost(
        post_url=message.text,
        message_id=message.message_id), user)
    insert_analytics(user, 'insta_link')


@bot.message_handler(regexp=r'^\{geo}'.format(geo=BASE_CMD_GEO))
@catch_bot_handler_error
def geo_start(message):
    user = get_user(user_id=message.chat.id)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(
        text="Send location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(
        user.user_id,
        "Hello! Click on the button and give me your location.",
        reply_markup=keyboard)
    insert_analytics(user, message.text)


@bot.message_handler(regexp=r'^\{virus}'.format(virus=BASE_CMD_VIRUS))
@catch_bot_handler_error
def virus(message):
    user = get_user(user_id=message.chat.id)

    sent_virus_data(user)
    insert_analytics(user, message.text)


@bot.message_handler(content_types=['location'])
@catch_bot_handler_error
def location(message):
    user = get_user(user_id=message.chat.id)

    if message.location is not None:
        send_map_location(bot, user, message)
    insert_analytics(user, message.text)


@bot.message_handler(
    content_types=[
        'text',
        'document'],
    func=lambda message: True)
@catch_bot_handler_error
def echo_all(message):
    user = get_user(user_id=message.chat.id)
    user_message = message.text

    logger().info("User message: '{}'".format(user_message))


@bot.callback_query_handler(func=lambda call: call.data == currency_graph)
@catch_bot_handler_error
def currency_graph(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    send_currency_graph(user, call.message)
    insert_analytics(user, currency_graph)


@bot.callback_query_handler(func=lambda call: call.data == cinema_soon)
@catch_bot_handler_error
def cinema_soon(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    send_cinema_soon_list(user)
    insert_analytics(user, call.data)


@bot.callback_query_handler(
    func=lambda call: call.data in football_leagues_cmd)
@catch_bot_handler_error
def football_calendar(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    send_football_calendar(user, call.data)
    insert_analytics(user, call.data)


if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except Exception as e:
        logger().error(e)

# bot.register_next_step_handler(message, func) #следующий шаг – функция
# func(message)
