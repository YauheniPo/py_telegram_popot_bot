from telegram import ParseMode

from base.bot.bot_config import location_atm
from base.bot.bot_constants import MSG_LOCATION_MAP
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
