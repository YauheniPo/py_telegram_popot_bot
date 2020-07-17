# -*- coding: utf-8 -*-
from telebot import types

from util.logger import logger


def get_message_keyboard(*args):
    message_keyboard = types.InlineKeyboardMarkup()
    for button in args:
        buttons = [
            types.InlineKeyboardButton(
                text=value,
                callback_data=key) for key,
            value in button.items()]
        message_keyboard.row(*buttons)
    logger().info("Get message keyboard: {}".format(args))
    return message_keyboard
