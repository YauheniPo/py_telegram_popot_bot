# -*- coding: utf-8 -*-

# Настройки
import apiai
import json
import configparser
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read(filenames='security_data.ini')

updater = Updater(token=settings.get(section='Tokens', option='bot_token'))  # Токен API к Telegram
dispatcher = updater.dispatcher


# Обработка команд
def start_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def url_builder(city):
    user_api_key = settings.get(section='Tokens', option='weather_api_key')  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?q='  # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
    full_api_url = api + city + '&mode=json&units=' + unit + '&APPID=' + user_api_key
    return full_api_url


def text_message(bot, update):
    request_smalltalk = apiai.ApiAI(client_access_token=settings.get('Tokens', 'apiai_smalltalk_token')).text_request()  # Токен API к Dialogflow
    request_weather = apiai.ApiAI(client_access_token=settings.get('Tokens', 'apiai_weather_token')).text_request()  # Токен API к Dialogflow
    request_smalltalk.lang = 'ru'  # На каком языке будет послан запрос
    request_weather.lang = 'ru'  # На каком языке будет послан запрос
    request_smalltalk.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request_weather.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request_smalltalk.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    request_weather.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
    response_json_talks = json.loads(request_smalltalk.getresponse().read().decode('utf-8'))
    response_json_weather = json.loads(request_weather.getresponse().read().decode('utf-8'))
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response_json_weather['result'].get('action'):
        r = requests.get(url_builder(response_json_weather['result']['parameters']['address']['city'])).json()
        bot.send_message(chat_id=update.message.chat_id, text=r)
        return
    response = response_json_talks['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
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
