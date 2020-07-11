import os

import telebot

TELEGRAM_BOT_TOKEN = os.environ.get('BOT_TOKEN')
TELEGRAM_BOT_NAME = os.environ.get('BOT_NAME')
bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN, threaded=False)
