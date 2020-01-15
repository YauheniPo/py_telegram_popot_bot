import logging

from telegram import ParseMode

from base.msg_context import *
from config import *
from features.currency.currency_api import fetch_currency_list, get_currency_response_json, get_currency_data_message
from features.instagram.insta_loader import get_insta_post_data, fetch_insta_post_content_files
from util.bot_helper import get_message_keyboard

logger = logging.getLogger(__name__)


def send_currency_rate(bot, user, actual_currency: int):
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
    insta_post = get_insta_post_data(user_message)

    logger.info(("--Instagram instance-- '{}'".format(insta_post.__dict__)).encode("utf-8"))

    try:
        fetch_insta_post_content_files(insta_post)
        send_to_user_insta_post_media_content(bot, insta_post, user)
    except:
        logger.error(u"{}: {}".format(error_msg_save_image, insta_post))
        bot.send_message(chat_id=user.user_id,
                         text=error_msg_save_image)
