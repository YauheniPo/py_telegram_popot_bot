import re

from telegram import ParseMode

from base.bot.bot import bot
from base.constants import MSG_CURRENCY_ALARM_BOT
from bot_config import buttons_currency_selection, button_currency_graph, currency_dollar_id, button_currency_alarm, \
    buttons_currency_alarm_rate, currency_alarm_rate_regexp, currency_ids, currency_graph_path
from db.db_connection import DBConnector
from features.currency.currency_api import get_currency_message, fetch_currency_list, get_currency_response_json, \
    get_actual_currency_rate_for_alarm
from features.currency.currency_graph_generator import fetch_currency_graph
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


def send_msg_alarm_currency(user):
    today_currency_rate, db_user_alarm_currency_rate = get_actual_currency_rate_for_alarm(
        user)

    bot.send_message(
        chat_id=user.user_id,
        text=MSG_CURRENCY_ALARM_BOT.format(
            today_rate=today_currency_rate,
            around_today_rate=round(db_user_alarm_currency_rate, 1)),
        reply_markup=get_message_keyboard(buttons_currency_alarm_rate),
        parse_mode=ParseMode.HTML)


def set_currency_alarm_rate(user, call):
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

    DBConnector().insert_currency_alarm(user, new_currency_alarm_rate)


def send_currency_graph(user, bot_message):
    actual_currency = list(
        set(currency_ids) - set([currency_data['callback_data']
                                 for currency_data in bot_message.json['reply_markup']['inline_keyboard'][1]]))[0]

    currency_data_bot = fetch_currency_list(
        get_currency_response_json(actual_currency))
    fetch_currency_graph(currency_data_bot)

    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[actual_currency]

    bot.send_photo(chat_id=user.user_id, reply_markup=get_message_keyboard(
        actual_buttons_currency_selection), photo=open(currency_graph_path, 'rb'))
