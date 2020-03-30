# -*- coding: utf-8 -*-
from telegram import ParseMode

from bot import bot
from bot_config import *
from features.currency.currency_api import get_currency_message
from features.instagram.insta_loader import fetch_insta_post_data
from features.location.geo import Geo
from features.location.map_fetcher import fetch_map
from util.bot_helper import get_message_keyboard


def send_currency_rate(bot, user, currency_id: int):
    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[currency_id]

    buttons = [button_currency_graph, actual_buttons_currency_selection]
    if currency_id == currency_dollar_id:
        buttons.append(button_currency_alarm)

    bot.send_message(chat_id=user.user_id,
                     text=get_currency_message(currency_id),
                     reply_markup=get_message_keyboard(*buttons),
                     parse_mode=ParseMode.HTML)


def send_to_user_insta_post_media_content(insta_post, user):
    fetch_insta_post_data(insta_post)

    bot.send_message(
        chat_id=user.user_id,
        reply_to_message_id=insta_post.message_id,
        text="<b>Post description</b>\n\n{}\n\n{}".format(insta_post.post_description, "\n\n".join(insta_post.media_urls)),
        parse_mode=ParseMode.HTML)


def send_map_location(bot, user, message):
    wait_message = bot.send_message(
        chat_id=user.user_id,
        reply_to_message_id=message.message_id,
        text="Data processing may take up to 15 seconds. Please wait.")

    geo = Geo(
        message.location.latitude,
        message.location.longitude,
        location_atm)
    fetch_map(geo)

    map_message = bot.send_photo(chat_id=user.user_id,
                                 reply_to_message_id=message.message_id,
                                 photo=open(geo.screen_path, 'rb'))
    bot.delete_message(chat_id=user.user_id,
                       message_id=wait_message.message_id)
    bot.send_message(
        chat_id=user.user_id,
        reply_to_message_id=map_message.message_id,
        text="<a href='{link}'>GO to Yandex map.\nClick here!</a>".format(
            link=geo.geo_map_url),
        parse_mode=ParseMode.HTML)
