# -*- coding: utf-8 -*-

import telebot
from telebot import types
from telegram import ParseMode

from features.cinema.cinema_site_parsing import *
from features.currency.currency_api import *
from features.currency.currency_graph_generate import fetch_currency_graph
from features.football.football_site_parsing import *
from features.instagram.insta_loader import *
from msg_context import *
from user import User
from util.util_parsing import is_match_by_regexp
from util.util_request import get_site_content

bot = telebot.TeleBot(token=os.environ.get('bot_token'))

users = dict()


def get_user(user_id=None, chat=None):
    if bool(os.environ.get('demo')):
        if user_id is None:
            return User(chat=chat)
        return User(user_id=user_id)

    if user_id is None:
        return users[chat.from_user.id]
    return users[user_id]


base_cmd_start = '/start'
base_cmd_currency = '/currency'
base_cmd_cinema = '/cinema'
base_cmd_football = '/football'
base_cmd_instagram = '/instagram'

logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.log',
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    format=u'%(asctime)s %(levelname)-8s %(name)-45s %(message)s',
                    level=logging.INFO)


def get_message_keyboard(*args):
    message_keyboard = types.InlineKeyboardMarkup()
    for button in args:
        buttons = [types.InlineKeyboardButton(text=key, callback_data=button[key]) for key in button]
        message_keyboard.row(*buttons)
    logger.info("Get message keyboard: {}".format(args))
    return message_keyboard


@bot.message_handler(regexp='^\{start}'.format(start=base_cmd_start))
def start(message):
    user = User(chat=message.chat)
    users[user.user_id] = user

    bot.send_message(chat_id=user.user_id,
                     text=start_base_cmd_text.format(start=base_cmd_start,
                                                     currency=base_cmd_currency,
                                                     cinema=base_cmd_cinema,
                                                     football=base_cmd_football,
                                                     instagram=base_cmd_instagram))


def fetch_currency(actual_currency: int, message):
    user = get_user(chat=message.chat)

    currency_list = fetch_currency_list(get_currency_response_json(actual_currency))

    currency_response_past_days = get_currency_data_message(currency_list[-10:-1])
    currency_response_current_day = get_currency_data_message([currency_list[-1]])

    current_currency = list(buttons_currency_selection.keys())[
        list(buttons_currency_selection.values()).index(actual_currency)]
    actual_buttons_currency_selection = dict(buttons_currency_selection)
    del actual_buttons_currency_selection[current_currency]

    bot.send_message(chat_id=user.user_id,
                     text=currency_bot_text.format(
                         currency=current_currency,
                         currency_past_days=currency_response_past_days,
                         currency_current_day=currency_response_current_day),
                     reply_markup=get_message_keyboard(button_currency_graph, actual_buttons_currency_selection),
                     parse_mode=ParseMode.HTML)


@bot.message_handler(regexp='^\{command}'.format(command=base_cmd_currency))
def currency(message):
    fetch_currency(config.currency_dollar_id, message)


@bot.message_handler(regexp='^\{cinema}'.format(cinema=base_cmd_cinema))
def cinema(message):
    user = get_user(chat=message.chat)

    movies = get_movies(get_site_content(config.cinema_url + config.cinema_url_path_today))

    bot.send_message(chat_id=user.user_id,
                     text=get_cinema_data_message(movies),
                     reply_markup=get_message_keyboard(button_cinema_soon),
                     parse_mode=ParseMode.HTML)


@bot.message_handler(regexp='^\{football}'.format(football=base_cmd_football))
def football(message):
    user = get_user(chat=message.chat)

    bot.send_message(chat_id=user.user_id,
                     text=football_base_cmd_text,
                     reply_markup=get_message_keyboard(buttons_football_leagues[0], buttons_football_leagues[1]))


@bot.message_handler(regexp='^\{instagram}'.format(instagram=base_cmd_instagram))
def instagram(message):
    user = get_user(chat=message.chat)

    bot.send_message(chat_id=user.user_id,
                     text=instagram_bot_text)


def send_instagram_media(user_message, user):
    logger.info("Instagram link '{}'".format(user_message))
    insta_post = get_insta_post_data(get_site_content(re.sub('.*w\.', '', user_message, 1)))

    if not insta_post.is_private_profile:
        try:
            fetch_insta_post_content_files(insta_post)
        except:
            logger.error(u"{}: {}".format(error_msg_save_image, insta_post))
            bot.send_message(chat_id=user.user_id,
                             text=error_msg_save_image)
            return

        for path in insta_post.media_content_path:
            logger.info("Send media '{}'".format(path))
            if insta_post.content_type == instagram_video_type:
                bot.send_video(chat_id=user.user_id,
                               data=open(path, 'rb'))
            elif insta_post.content_type == instagram_image_type:
                bot.send_photo(chat_id=user.user_id,
                               photo=open(path, 'rb'))

        if insta_post.post_description:
            bot.send_message(chat_id=user.user_id,
                             text="<b>Post description</b>\n\n" + insta_post.post_description[0]['node']['text'],
                             parse_mode=ParseMode.HTML)
    else:
        bot.send_message(chat_id=user.user_id,
                         text=instagram_warning_text_not_public)


@bot.message_handler(content_types=['text', 'document'], func=lambda message: True)
def echo_all(message):
    user = get_user(chat=message.chat)

    user_message = message.text
    logger.info("User message: '{}'".format(user_message))

    if user_message is not None and is_match_by_regexp(user_message, instagram_link_regexp):
        send_instagram_media(user_message, user)


# bot.register_next_step_handler(message, func) #следующий шаг – функция func(message)

# base_buttons = ReplyKeyboardMarkup(resize_keyboard=True)  # под клавиатурой
# base_buttons.add(KeyboardButton(base_cmd_currency), KeyboardButton(base_cmd_start))


@bot.callback_query_handler(func=lambda call: True)  # обработчик кнопок
def callback_worker(call):
    logger.info("Button '{}'".format(call.data))
    user = get_user(call.from_user.id)

    dict_buttons_football = dict((key, d[key]) for d in buttons_football_leagues for key in d)

    if call.data in [str(currency_id) for currency_id in buttons_currency_selection.values()]:
        fetch_currency(call.data, call.message)

    elif call.data == currency_graph:
        actual_currency = list(set(buttons_currency_selection.keys()) - set([
            currency_data['text']
            for currency_data in call.message.json['reply_markup']['inline_keyboard'][1]]))[0]

        currency_data_bot = fetch_currency_list(get_currency_response_json(buttons_currency_selection[actual_currency]))
        fetch_currency_graph(currency_data_bot)

        actual_buttons_currency_selection = dict(buttons_currency_selection)
        del actual_buttons_currency_selection[actual_currency]

        bot.send_photo(chat_id=user.user_id,
                       reply_markup=get_message_keyboard(actual_buttons_currency_selection),
                       photo=open(currency_graph_path, 'rb'))

    elif call.data == cinema_soon:
        movies = get_movies(get_site_content(url=config.cinema_url + config.cinema_url_path_soon,
                                             params=cinema_soon_params))
        bot.send_message(chat_id=user.user_id,
                         text=get_cinema_data_message(movies),
                         parse_mode=ParseMode.HTML)

    elif call.data in dict_buttons_football.values():
        matches = get_matches(get_site_content(url=config.football_url + call.data + config.football_url_path_calendar))
        football_message_title = [key for key, value in dict_buttons_football.items() if value == call.data][0]

        actual_buttons_football = dict(dict_buttons_football)
        del actual_buttons_football[football_message_title]

        bot.send_message(chat_id=user.user_id,
                         text="<b>{}</b>\n\n".format(football_message_title) + get_football_data_message(matches),
                         reply_markup=get_message_keyboard(actual_buttons_football),
                         parse_mode=ParseMode.HTML)


bot.polling(none_stop=True)
