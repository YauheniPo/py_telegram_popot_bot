# -*- coding: utf-8 -*-

import logging
import os

import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telegram import ParseMode

from config import currency_graph_path
from features.currency.currency_api import fetch_currency_list, get_currency_response_json, get_currency_data_message
from features.currency.graph import fetch_currency_graph
from user import User
from util.util_date import currency_msg_date_format

base_cmd_start = '/start'
base_cmd_currency = '/currency'

logging.basicConfig(filename='log.log', datefmt='%d/%m/%Y %I:%M:%S %p',
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                    level=logging.INFO)

bot = telebot.TeleBot(token=os.environ.get('bot_token'))

base_buttons = ReplyKeyboardMarkup(resize_keyboard=True)  # под клавиатурой
base_buttons.add(KeyboardButton(base_cmd_currency), KeyboardButton(base_cmd_start))


def init_user(message):
    user = User(message.from_user.first_name, message.from_user.last_name, message.from_user.username,
                message.from_user.id, message.from_user.language_code, message)
    logging.info(user)
    return user


def start(user):
    bot.send_message(chat_id=user.user_id, text='Привет {username}, давай пообщаемся?'.format(username=user.username))


@bot.message_handler(regexp='^\{command}'.format(command=base_cmd_currency))
def get_currency(message):
    user = init_user(message)

    currency_data_bot = fetch_currency_list(get_currency_response_json())

    bot_text_response_past_days = get_currency_data_message(currency_data_bot[-10:-1], currency_msg_date_format)
    bot_text_response_current_day = get_currency_data_message([currency_data_bot[-1]], currency_msg_date_format)

    currency_graph_keyboard = types.InlineKeyboardMarkup()
    currency_graph_button = types.InlineKeyboardButton(text='Currency Graph', callback_data='currency_graph')
    currency_graph_keyboard.add(currency_graph_button)

    bot.send_message(chat_id=user.user_id,
                     text=
'''<i>{bot_text_response_past_days}</i>

<b>{bot_text_response_current_day}</b>'''.format(
                         bot_text_response_past_days=bot_text_response_past_days,
                         bot_text_response_current_day=bot_text_response_current_day),
                     reply_markup=currency_graph_keyboard,
                     parse_mode=ParseMode.HTML)


command_dict = {base_cmd_start: start, base_cmd_currency: None}


@bot.message_handler(content_types=['text', 'document'], func=lambda message: True)
def echo_all(message):
    user = init_user(message)

    if message.text in command_dict:
        command_dict[message.text](user=user)
    else:
        bot.send_message(chat_id=user.user_id, text=message.text)
        # bot.register_next_step_handler(message, func) #следующий шаг – функция func(message)

        # keyboard = types.InlineKeyboardMarkup()  # наша клавиатура под сообщением
        # key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        # keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        # key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        # keyboard.add(key_no)

        # bot.send_message(reply_markup=btn)

        # bot.send_message(chat_id=user.user_id, text="Hi")


@bot.callback_query_handler(func=lambda call: True)  # обработчик кнопок
def callback_worker(call):
    if call.data == "currency_graph":
        currency_data_bot = fetch_currency_list(get_currency_response_json())

        fetch_currency_graph(currency_data_bot)
        bot.send_photo(chat_id=call.from_user.id, photo=open(currency_graph_path, 'rb'))


bot.polling(none_stop=True)
