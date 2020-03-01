from telegram import ParseMode

from bot_config import *
from bot_constants import *
from features.currency.currency_api import fetch_currency_list, get_currency_response_json, get_currency_data_message
from features.instagram.insta_loader import get_insta_post_data, fetch_insta_post_content_files
from features.location.geo import Geo
from features.location.map_fetcher import fetch_map
from logger import logger
from util.bot_helper import get_message_keyboard


def send_currency_rate(bot, user, actual_currency: int):
    currency_list = fetch_currency_list(get_currency_response_json(actual_currency))

    currency_response_past_days = get_currency_data_message(currency_list[-10:-1])
    currency_response_current_day = get_currency_data_message([currency_list[-1]])

    current_currency = buttons_currency_selection[actual_currency]
    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[actual_currency]

    bot.send_message(chat_id=user.user_id,
                     text=MSG_CURRENCY_BOT.format(
                         currency=current_currency,
                         currency_past_days=currency_response_past_days,
                         currency_current_day=currency_response_current_day),
                     reply_markup=get_message_keyboard(button_currency_graph, actual_buttons_currency_selection),
                     parse_mode=ParseMode.HTML)


def send_to_user_insta_post_media_content(bot, insta_post, user):
    for content_type, content_path in zip(insta_post.media_types, insta_post.media_content_paths):
        logger().info("Send media '{}'".format(content_path))
        if content_type == instagram_video_type:
            bot.send_video(chat_id=user.user_id,
                           reply_to_message_id=insta_post.message_id,
                           data=open(content_path, 'rb'))
        elif content_type == instagram_image_type:
            bot.send_photo(chat_id=user.user_id,
                           reply_to_message_id=insta_post.message_id,
                           photo=open(content_path, 'rb'))
        else:
            bot.send_message(chat_id=user.user_id,
                             reply_to_message_id=insta_post.message_id,
                             text=MSG_WARNING_INSTAGRAM_UNKNOWN_CONTENT_TYPE)

    if insta_post.post_description:
        bot.send_message(chat_id=user.user_id,
                         reply_to_message_id=insta_post.message_id,
                         text="<b>Post description</b>\n\n" + insta_post.post_description[0]['node']['text'],
                         parse_mode=ParseMode.HTML)


def send_instagram_media(bot, user_message, user):
    logger().info("Instagram link '{}'".format(user_message.text))
    insta_post = get_insta_post_data(user_message)

    logger().info(("--Instagram instance-- '{}'".format(insta_post.__dict__)).encode("utf-8"))

    if insta_post.is_blocked_profile:
        bot.send_message(chat_id=user.user_id,
                         reply_to_message_id=user_message.message_id,
                         text=MSG_ERROR_LINK_IS_BLOCKED)
    else:
        try:
            fetch_insta_post_content_files(insta_post)
            send_to_user_insta_post_media_content(bot, insta_post, user)
        except:
            logger().error(u"{}: {}".format(MSG_ERROR_MSG_SAVE_IMAGE, insta_post))
            bot.send_message(chat_id=user.user_id,
                             reply_to_message_id=user_message.message_id,
                             text=MSG_ERROR_MSG_SAVE_IMAGE)


def send_map_location(bot, user, message):
    wait_message = bot.send_message(chat_id=user.user_id,
                                    reply_to_message_id=message.message_id,
                                    text="Data processing may take up to 15 seconds. Please wait.")

    geo = Geo(message.location.latitude, message.location.longitude, location_atm)
    fetch_map(geo)

    map_message = bot.send_photo(chat_id=user.user_id,
                                 reply_to_message_id=message.message_id,
                                 photo=open(geo.screen_path, 'rb'))
    bot.delete_message(chat_id=user.user_id,
                       message_id=wait_message.message_id)
    bot.send_message(chat_id=user.user_id,
                     reply_to_message_id=map_message.message_id,
                     text="<a href='{link}'>GO to Yandex map.\nClick here!</a>".format(link=geo.geo_map_url),
                     parse_mode=ParseMode.HTML)
