# -*- coding: utf-8 -*-

import logging
import os

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import currency_graph_path
from features.currency.currency_api import fetch_currency_list, get_currency_response_json
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

    currency_data = fetch_currency_list(get_currency_response_json())
    currency_data_for_text = currency_data[-10:]

    bot_text_response = "\n".join(
        ["{day} -    {rate} BYR".format(day=currency_day.Date.strftime(currency_msg_date_format), rate=currency_day.Cur_OfficialRate)
         for currency_day in currency_data_for_text])

    bot.send_message(chat_id=user.user_id, text=bot_text_response)
    fetch_currency_graph(currency_data)
    bot.send_photo(chat_id=user.user_id, photo=open(currency_graph_path, 'rb'))


command_dict = {base_cmd_start: start, base_cmd_currency: None}


@bot.message_handler(content_types=['text', 'document'], func=lambda message: True)
def echo_all(message):
    user = init_user(message)

    if message.text in command_dict:
        command_dict[message.text](user=user)
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
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        # код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню')
    elif call.data == "no":
        print('x')
        # переспрашиваем


bot.polling(none_stop=True, interval=0)

# # Хендлеры
# start_command_handler = CommandHandler(command='start', callback=start_command)
# text_message_handler = MessageHandler(filters=Filters.text, callback=text_message)
# # Добавляем хендлеры в диспетчер
# dispatcher.add_handler(handler=start_command_handler)
# dispatcher.add_handler(handler=text_message_handler)
# # Начинаем поиск обновлений
# updater.start_polling(clean=True)
# # Останавливаем бота, если были нажаты Ctrl + C
# updater.idle()
