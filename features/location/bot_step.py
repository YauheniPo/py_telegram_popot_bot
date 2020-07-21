from telebot import types
from telegram import ParseMode

from base.bot.bot import bot
from bot_config import location_atm
from base.constants import MSG_LOCATION_MAP, EMOJI_LOCATION, EMOJI_FINGER_DOWN
from features.location.geo import Geo
from features.location.map_fetcher import fetch_map


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
        text=MSG_LOCATION_MAP.format(link=geo.geo_map_url),
        parse_mode=ParseMode.HTML)


def geo_request(user):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(
        text=f"{EMOJI_LOCATION} Send location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(
        user.user_id,
        f"{EMOJI_LOCATION} Hello! Click on the button and give me your location.    {EMOJI_FINGER_DOWN}",
        reply_markup=keyboard)
