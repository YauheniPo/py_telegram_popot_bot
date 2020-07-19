# -*- coding: utf-8 -*-
from functools import wraps

from base.bot.bot import bot
from base.constants import MSG_START_CMD_BASE
from util.logger import logger


def catch_bot_handler_error(f):
    @wraps(f)
    def bot_handler_wrapper(bot_request):
        try:
            return f(bot_request)
        except Exception as e:
            # Add info to error tracking
            logger().exception(str(e))

    return bot_handler_wrapper


def start_step(user):
    bot.send_message(
        chat_id=user.user_id,
        text=MSG_START_CMD_BASE)
