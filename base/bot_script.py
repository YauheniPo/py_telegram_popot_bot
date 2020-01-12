import logging
import re

from telebot import types
from telegram import ParseMode

from base.msg_context import *
from config import *
from features.currency.currency_api import fetch_currency_list, get_currency_response_json, get_currency_data_message
from features.instagram.insta_loader import get_insta_post_data, fetch_insta_post_content_files
from util.util_request import get_site_content

logger = logging.getLogger(__name__)


def get_message_keyboard(*args):
    message_keyboard = types.InlineKeyboardMarkup()
    for button in args:
        buttons = [types.InlineKeyboardButton(text=key, callback_data=button[key]) for key in button]
        message_keyboard.row(*buttons)
    logger.info("Get message keyboard: {}".format(args))
    return message_keyboard


def fetch_currency(bot, user, actual_currency: int):
    currency_list = fetch_currency_list(get_currency_response_json(actual_currency))

    currency_response_past_days = get_currency_data_message(currency_list[-10:-1])
    currency_response_current_day = get_currency_data_message([currency_list[-1]])

    current_currency = list(buttons_currency_selection.keys())[
        list(buttons_currency_selection.values()).index(actual_currency)]
    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[current_currency]

    bot.send_message(chat_id=user.user_id,
                     text=currency_bot_text.format(
                         currency=current_currency,
                         currency_past_days=currency_response_past_days,
                         currency_current_day=currency_response_current_day),
                     reply_markup=get_message_keyboard(button_currency_graph, actual_buttons_currency_selection),
                     parse_mode=ParseMode.HTML)


def send_to_user_insta_post_media_content(bot, insta_post, user):
    for content_type, content_path in zip(insta_post.media_types, insta_post.media_content_paths):
        logger.info("Send media '{}'".format(content_path))
        if content_type == instagram_video_type:
            bot.send_video(chat_id=user.user_id,
                           data=open(content_path, 'rb'))
        elif content_type == instagram_image_type:
            bot.send_photo(chat_id=user.user_id,
                           photo=open(content_path, 'rb'))
        else:
            bot.send_message(chat_id=user.user_id,
                             text=instagram_warning_unknown_content_type)

    if insta_post.post_description:
        bot.send_message(chat_id=user.user_id,
                         text="<b>Post description</b>\n\n" + insta_post.post_description[0]['node']['text'],
                         parse_mode=ParseMode.HTML)


def send_instagram_media(bot, user_message, user):
    logger.info("Instagram link '{}'".format(user_message))
    insta_post = get_insta_post_data(get_site_content(re.sub('.*w\.', '', user_message, 1)))

    logger.info("--Instagram instance-- '{}'".format(insta_post.__dict__))

    if not insta_post.is_private_profile:
        try:
            fetch_insta_post_content_files(insta_post)
            send_to_user_insta_post_media_content(bot, insta_post, user)
        except:
            logger.error(u"{}: {}".format(error_msg_save_image, insta_post))
            bot.send_message(chat_id=user.user_id,
                             text=error_msg_save_image)
    else:
        bot.send_message(chat_id=user.user_id,
                         text=instagram_warning_text_not_public)
