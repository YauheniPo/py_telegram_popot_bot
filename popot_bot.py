# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telegram import ParseMode

from base.bot_script import send_currency_rate, get_message_keyboard, send_instagram_media, send_map_location
from base.user import User
from constants_bot import *
from features.cinema.cinema_site_parser import *
from features.currency.currency_api import *
from features.currency.currency_graph_generator import fetch_currency_graph
from features.football.football_site_parser import *
from features.instagram.insta_loader import *
from util.util_parsing import is_match_by_regexp
from util.util_request import get_site_request_content

TELEGRAM_BOT_TOKEN = os.environ.get('bot_token')
bot = telebot.TeleBot(token=TELEGRAM_BOT_TOKEN, threaded=False)

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    format=u'%(asctime)s %(levelname)-8s %(name)-45s %(message)s',
                    level=logging.INFO)

users = dict()


def get_user(user_id=None, chat=None):
    if bool(os.environ.get('demo')):
        if user_id is None:
            return User(chat=chat)
        return User(user_id=user_id)

    if user_id is None:
        return users[chat.from_user.id]
    return users[user_id]


@bot.message_handler(regexp='^\{start}'.format(start=BASE_CMD_START))
def start(message):
    user = User(chat=message.chat)
    users[user.user_id] = user

    bot.send_message(chat_id=user.user_id,
                     text=MSG_START_CMD_BASE.format(start=BASE_CMD_START,
                                                    currency=BASE_CMD_CURRENCY,
                                                    cinema=BASE_CMD_CINEMA,
                                                    football=BASE_CMD_FOOTBALL,
                                                    instagram=BASE_CMD_INSTAGRAM,
                                                    geo=BASE_CMD_GEO))


@bot.message_handler(regexp='^\{command}'.format(command=BASE_CMD_CURRENCY))
@bot.callback_query_handler(func=lambda call: call.data in currency_list)
def currency(message):
    if type(message) == Message:
        chat = message.chat
        actual_currency = config.currency_dollar_id
    else:
        chat = message.message.chat
        actual_currency = message.data

    user = get_user(chat=chat)

    send_currency_rate(bot, user, actual_currency)


@bot.message_handler(regexp='^\{cinema}'.format(cinema=BASE_CMD_CINEMA))
def cinema(message):
    user = get_user(chat=message.chat)

    movies = get_movies(get_site_request_content(config.cinema_url + config.cinema_url_path_today))

    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     reply_markup=get_message_keyboard(button_cinema_soon),
                     parse_mode=ParseMode.HTML)


@bot.message_handler(regexp='^\{football}'.format(football=BASE_CMD_FOOTBALL))
def football(message):
    user = get_user(chat=message.chat)

    bot.send_message(chat_id=user.user_id,
                     text=MSG_FOOTBALL_BASE_CMD,
                     reply_markup=get_message_keyboard(buttons_football_leagues[0], buttons_football_leagues[1]))


@bot.message_handler(regexp='^\{instagram}'.format(instagram=BASE_CMD_INSTAGRAM))
def instagram(message):
    user = get_user(chat=message.chat)

    bot.send_message(chat_id=user.user_id,
                     text=MSG_INSTAGRAM_BOT)


@bot.message_handler(regexp='^\{geo}'.format(geo=BASE_CMD_GEO))
def geo(message):
    user = get_user(chat=message.chat)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send location", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(user.user_id, "Hello! Click on the button and give me your location.", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    user = get_user(chat=message.chat)

    if message.location is not None:
        send_map_location(bot, user, message)


@bot.message_handler(
    func=lambda message: message.text is not None and is_match_by_regexp(message.text, instagram_link_regexp))
def send_instagram_post_content(message):
    user = get_user(chat=message.chat)

    user_message = message.text
    logger.info("User message: '{}'".format(user_message))

    send_instagram_media(bot, message, user)


@bot.message_handler(content_types=['text', 'document'], func=lambda message: True)
def echo_all(message):
    user = get_user(chat=message.chat)

    user_message = message.text
    logger.info("User message: '{}'".format(user_message))


@bot.callback_query_handler(func=lambda call: call.data == currency_graph)
def send_currency_graph(call):
    logger.info("Button '{}'".format(call.data))
    user = get_user(call.from_user.id)

    actual_currency = list(
        set(buttons_currency_selection.keys()) -
        set([currency_data['text'] for currency_data in call.message.json['reply_markup']['inline_keyboard'][1]]))[0]

    currency_data_bot = fetch_currency_list(get_currency_response_json(buttons_currency_selection[actual_currency]))
    fetch_currency_graph(currency_data_bot)

    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[actual_currency]

    bot.send_photo(chat_id=user.user_id,
                   reply_markup=get_message_keyboard(actual_buttons_currency_selection),
                   photo=open(currency_graph_path, 'rb'))


@bot.callback_query_handler(func=lambda call: call.data == cinema_soon)
def send_cinema_soon(call):
    logger.info("Button '{}'".format(call.data))
    user = get_user(call.from_user.id)

    movies = get_movies(get_site_request_content(url=config.cinema_url + config.cinema_url_path_soon,
                                                 params=cinema_soon_params))
    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     parse_mode=ParseMode.HTML)


@bot.callback_query_handler(func=lambda call: call.data in dict_buttons_football.values())
def send_football_calendar(call):
    logger.info("Button '{}'".format(call.data))
    user = get_user(call.from_user.id)

    matches = get_matches(get_site_request_content(
        url=config.football_url + call.data + config.football_url_path_calendar))
    football_message_title = [key for key, value in dict_buttons_football.items() if value == call.data][0]

    actual_buttons_football = dict(dict_buttons_football)
    del actual_buttons_football[football_message_title]

    bot.send_message(chat_id=user.user_id,
                     text="<b>{}</b>\n\n".format(football_message_title) + get_football_data_message(matches),
                     reply_markup=get_message_keyboard(actual_buttons_football),
                     parse_mode=ParseMode.HTML)


if __name__ == "__main__":
    for i in range(0, 5):
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(e)

# bot.set_webhook("https://{}.pythonanywhere.com/{}".format(os.environ.get('username'), TELEGRAM_BOT_TOKEN))

# bot.register_next_step_handler(message, func) #следующий шаг – функция func(message)

# base_buttons = ReplyKeyboardMarkup(resize_keyboard=True)  # под клавиатурой
# base_buttons.add(KeyboardButton(base_cmd_currency), KeyboardButton(base_cmd_start))
