import re

from telegram import ParseMode

from base.bot.bot import bot
from base.bot.bot_config import buttons_currency_selection, button_currency_graph, currency_dollar_id, button_currency_alarm, \
    buttons_currency_alarm_rate, currency_alarm_rate_regexp
from base.bot.bot_constants import MSG_CURRENCY_ALARM_BOT
from features.currency.currency_api import get_currency_message
from util.bot_helper import get_message_keyboard
from util.util_data import find_all_by_regexp


def send_currency_rate(user, currency_id: int):
    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[currency_id]

    buttons = [button_currency_graph, actual_buttons_currency_selection]
    if currency_id == currency_dollar_id:
        buttons.append(button_currency_alarm)

    bot.send_message(chat_id=user.user_id,
                     text=get_currency_message(currency_id),
                     reply_markup=get_message_keyboard(*buttons),
                     parse_mode=ParseMode.HTML)


def send_msg_alarm_currency(user, today_currency_rate, around_today_currency_rate):
    bot.send_message(
        chat_id=user.user_id,
        text=MSG_CURRENCY_ALARM_BOT.format(
            today_rate=today_currency_rate,
            around_today_rate=around_today_currency_rate),
        reply_markup=get_message_keyboard(buttons_currency_alarm_rate),
        parse_mode=ParseMode.HTML)


def set_currency_alarm_rate_and_get_new_rate(call):
    call_message = call.message.text.strip()
    currency_alarm_rate = find_all_by_regexp(
        call_message, currency_alarm_rate_regexp)[0]
    new_currency_alarm_rate = round(eval(currency_alarm_rate + call.data), 1)
    new_currency_alarm_rate_for_replace = "<b>{}</b>".format(
        new_currency_alarm_rate)
    message = re.sub(
        currency_alarm_rate_regexp,
        new_currency_alarm_rate_for_replace,
        call_message)

    def send_currency_alarm_message(message):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=message,
            reply_markup=get_message_keyboard(buttons_currency_alarm_rate),
            parse_mode=ParseMode.HTML)

    send_currency_alarm_message(message)

    return new_currency_alarm_rate
