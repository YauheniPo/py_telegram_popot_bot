# -*- coding: utf-8 -*-

# Настройки
import json
import apiai
import pyowm
import requests
import telebot
from pyowm.exceptions import api_response_error
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from configparser import ExtendedInterpolation, ConfigParser
import logging

from user import User, OnlyOne

logging.basicConfig(filename='log.log', datefmt='%d/%m/%Y %I:%M:%S %p',
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', level=logging.INFO)
settings = ConfigParser()
settings._interpolation = ExtendedInterpolation()
settings.read(filenames='security_data.ini')
bot = telebot.TeleBot(token=settings.get(section='Tokens', option='bot_token'))


def get_weather(city):
    owm = pyowm.OWM(API_key=settings.get(section='Tokens', option='weather_api_key'), language='ru')
    try:
        observation = owm.weather_at_place(name=city)
    except api_response_error.NotFoundError:
        return "The searched item was not found."
    return observation.get_weather().get_temperature('celsius')


def init_user(data, text):
    user = User(data.first_name, data.last_name, data.username, data.id, data.language_code, text)
    logging.info(user)
    return user


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = init_user(message.from_user, message.text)

    bot.reply_to(message=message, text='Привет {username}, давай пообщаемся?'.format(username=user.get_username()))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user = init_user(message.from_user, message.text)

    request_smalltalk = apiai.ApiAI(
        client_access_token=settings.get('Tokens', 'apiai_smalltalk_token')).text_request()  # Токен API к Dialogflow
    request_weather = apiai.ApiAI(
        client_access_token=settings.get('Tokens', 'apiai_weather_token')).text_request()  # Токен API к Weather
    request_smalltalk.lang = user.get_lang()  # На каком языке будет послан запрос
    request_weather.lang = user.get_lang()  # На каком языке будет послан запрос
    request_smalltalk.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request_weather.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request_smalltalk.query = message.text  # Посылаем запрос к ИИ с сообщением от юзера
    request_weather.query = message.text  # Посылаем запрос к ИИ с сообщением от юзера
    response_json_talks = json.loads(s=request_smalltalk.getresponse().read().decode('utf-8'))
    response_json_weather = json.loads(s=request_weather.getresponse().read().decode('utf-8'))

    if response_json_weather['result'].get('action'):
        # r = requests.get(url='http://api.openweathermap.org/data/2.5/weather', params={
        #                  'q': response_json_weather['result']['parameters']['address']['city'],
        #                  'lang': 'ru', 'mode': 'json', 'units': 'metric',
        #                  'APPID': settings.get(section='Tokens', option='weather_api_key')}).json()
        w = get_weather(city=response_json_weather['result']['parameters']['address']['city'])
        bot.reply_to(message=message, text=json.dumps(w))
        return

    response = response_json_talks['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    if not response:
        response = 'Я Вас не совсем понял!'
    bot.reply_to(message=message, text=response)


bot.polling(none_stop=True, timeout=123)

# settings = configparser.ConfigParser()
# settings._interpolation = configparser.ExtendedInterpolation()
# settings.read(filenames='security_data.ini')
#
# updater = Updater(token=settings.get(section='Tokens', option='bot_token'))  # Токен API к Telegram
# dispatcher = updater.dispatcher
#
#
# # Обработка команд
# def start_command(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
#
#
# # def url_builder(city):
# #     user_api_key = settings.get(section='Tokens', option='weather_api_key')  # Obtain yours form: http://openweathermap.org/
# #     unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
# #     api = 'http://api.openweathermap.org/data/2.5/weather?q='  # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
# #     full_api_url = api + city + '&mode=json&units=' + unit + '&APPID=' + user_api_key
# #     return full_api_url
#
#
# def get_weather(city):
#     owm = pyowm.OWM(API_key=settings.get(section='Tokens', option='weather_api_key'), language='ru')
#     observation = owm.weather_at_place(name=city)
#     return observation.get_weather().get_temperature('celsius')
#
#
# def text_message(bot, update):
#     request_smalltalk = apiai.ApiAI(client_access_token=settings.get('Tokens', 'apiai_smalltalk_token')).text_request()  # Токен API к Dialogflow
#     request_weather = apiai.ApiAI(client_access_token=settings.get('Tokens', 'apiai_weather_token')).text_request()  # Токен API к Dialogflow
#     request_smalltalk.lang = 'ru'  # На каком языке будет послан запрос
#     request_weather.lang = 'ru'  # На каком языке будет послан запрос
#     request_smalltalk.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
#     request_weather.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
#     request_smalltalk.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
#     request_weather.query = update.message.text  # Посылаем запрос к ИИ с сообщением от юзера
#     response_json_talks = json.loads(s=request_smalltalk.getresponse().read().decode('utf-8'))
#     response_json_weather = json.loads(s=request_weather.getresponse().read().decode('utf-8'))
#     # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
#     if response_json_weather['result'].get('action'):
#         w = get_weather(city=response_json_weather['result']['parameters']['address']['city'])
#         r = requests.get(url='http://api.openweathermap.org/data/2.5/weather', params={
#                          'q': response_json_weather['result']['parameters']['address']['city'],
#                          'lang': 'ru', 'mode': 'json', 'units': 'metric',
#                          'APPID': settings.get(section='Tokens', option='weather_api_key')}).json()
#         bot.send_message(chat_id=update.message.chat_id, text=r['weather'])
#         return
#     response = response_json_talks['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
#     if response:
#         bot.send_message(chat_id=update.message.chat_id, text=response)
#     else:
#         bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
#
#     # response = 'Получил Ваше сообщение: ' + update.message.text
#     # bot.send_message(chat_id=update.message.chat_id, text=response)
#
#
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
