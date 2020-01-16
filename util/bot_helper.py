# -*- coding: utf-8 -*-
import logging

from telebot import types

logger = logging.getLogger(__name__)


def get_message_keyboard(*args):
    message_keyboard = types.InlineKeyboardMarkup()
    for button in args:
        buttons = [types.InlineKeyboardButton(text=key, callback_data=button[key]) for key in button]
        message_keyboard.row(*buttons)
    logger.info("Get message keyboard: {}".format(args))
    return message_keyboard
