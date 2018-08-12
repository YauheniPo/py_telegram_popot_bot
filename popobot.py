# -*- coding: utf-8 -*-

# Настройки
import apiai
import json
import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read(filenames='security_data.ini')

updater = Updater(token=settings.get(section='Tokens', option='bot_token'))  # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def text_message(bot, update):
    request = apiai.ApiAI(client_access_token=settings.get('Tokens', 'apiai_token')).text_request()  # Токен API к Dialogflow
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')

    # response = 'Получил Ваше сообщение: ' + update.message.text
    # bot.send_message(chat_id=update.message.chat_id, text=response)


# Хендлеры
start_command_handler = CommandHandler(command='start', callback=start_command)
text_message_handler = MessageHandler(filters=Filters.text, callback=text_message)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(handler=start_command_handler)
dispatcher.add_handler(handler=text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
