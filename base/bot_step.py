# -*- coding: utf-8 -*-

from bot import bot
from bot_constants import *


def start_step(user):
    bot.send_message(
        chat_id=user.user_id,
        text=MSG_START_CMD_BASE.format(
            start=BASE_CMD_START,
            currency=BASE_CMD_CURRENCY,
            cinema=BASE_CMD_CINEMA,
            football=BASE_CMD_FOOTBALL,
            instagram=BASE_CMD_INSTAGRAM,
            geo=BASE_CMD_GEO,
            virus=BASE_CMD_VIRUS))
