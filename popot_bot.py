# -*- coding: utf-8 -*-
import bot_config
from base.bot.bot import bot
from base.bot.bot_step import start_step, catch_bot_handler_error
from base.constants import BASE_CMD_START, BASE_CMD_CURRENCY, DB_LOG_CMD, BASE_CMD_CINEMA, BASE_CMD_FOOTBALL, \
    MSG_FOOTBALL_BASE_CMD, BASE_CMD_INSTAGRAM, MSG_INSTAGRAM_BOT, BASE_CMD_GEO, BASE_CMD_VIRUS
from base.models.user import fetch_user, get_user
from db.db_connection import get_db_all_data, insert_analytics
from features.cinema.bot_step import send_cinema_list, send_cinema_soon_list
from features.currency.bot_step import send_currency_rate, send_msg_alarm_currency, \
    set_currency_alarm_rate, send_currency_graph
from features.football.bot_step import send_football_calendar
from features.instagram.bot_step import send_to_user_insta_post_media_content
from features.instagram.insta_post import InstaPost
from features.location.bot_step import send_map_location, geo_request
from features.virus.bot_step import sent_virus_data
from util.bot_helper import get_message_keyboard
from util.logger import logger
from util.util_data import is_match_by_regexp

__author__ = "Yauheni Papovich"
__email__ = "ip.popovich.1990@gmail.com"

__all__ = [
    'start',
    'currency_start',
    'currency_alarm_call',
    'currency_graph_call',
    'currency_alarm_rate_update',
    'cinema',
    'cinema_soon_call',
    'football_start',
    'football_calendar',
    'geo_start',
    'instagram_start',
    'instagram_post_content',
    'location',
    'virus',
    'echo_all',
    'db_log'
]


@bot.message_handler(regexp=r'^\{start}'.format(start=BASE_CMD_START))
@catch_bot_handler_error
def start(message):
    user = fetch_user(chat=message.chat)

    start_step(user)
    insert_analytics(user, message.text)


@bot.message_handler(regexp=r'^\{command}'.format(command=BASE_CMD_CURRENCY))
@bot.callback_query_handler(
    func=lambda call: call.data in bot_config.currency_ids)
@catch_bot_handler_error
def currency_start(message):
    user = get_user(message=message)

    actual_currency = getattr(message, 'data', bot_config.currency_dollar_id)
    send_currency_rate(user, actual_currency)
    insert_analytics(user, BASE_CMD_CURRENCY)


@bot.message_handler(regexp=r'^\{log}'.format(log=DB_LOG_CMD))
@catch_bot_handler_error
def db_log(message):
    user = get_user(user_id=message.chat.id)

    bot.send_message(user.user_id, str(get_db_all_data()))
    insert_analytics(user, message.text)


@bot.callback_query_handler(
    func=lambda call: call.data in bot_config.currency_alarm)
@catch_bot_handler_error
def currency_alarm_call(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    send_msg_alarm_currency(user)


@bot.callback_query_handler(
    func=lambda call: call.data is not None and is_match_by_regexp(
        call.data, bot_config.currency_alarm_rate_button_regexp))
@catch_bot_handler_error
def currency_alarm_rate_update(call):
    user = get_user(user_id=call.from_user.id)

    set_currency_alarm_rate(user, call)


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
                                                                     v) in
                                                         bot_config.buttons_football_leagues.items()]))
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
        message.text, bot_config.instagram_link_regexp))
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

    geo_request(user)
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


@bot.callback_query_handler(
    func=lambda call: call.data == bot_config.currency_graph)
@catch_bot_handler_error
def currency_graph_call(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    send_currency_graph(user, call.message)
    insert_analytics(user, bot_config.currency_graph)


@bot.callback_query_handler(
    func=lambda call: call.data == bot_config.cinema_soon)
@catch_bot_handler_error
def cinema_soon_call(call):
    logger().info("Button '{}'".format(call.data))
    user = get_user(user_id=call.from_user.id)

    send_cinema_soon_list(user)
    insert_analytics(user, call.data)


@bot.callback_query_handler(
    func=lambda call: call.data in bot_config.football_leagues_cmd)
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
