from telegram import ParseMode

import bot_config
from base.bot.bot import bot
from features.football.football_site_parser import get_matches, get_football_data_message
from util.bot_helper import get_message_keyboard
from util.util_request import get_site_request_content


def sent_football_message(user, message, buttons, parse_mode=None):
    bot.send_message(
        chat_id=user.user_id,
        text=message,
        reply_markup=buttons,
        parse_mode=parse_mode)


def send_football_calendar(user, football_league):
    matches = get_matches(get_site_request_content(
        url=f"{bot_config.football_url}{football_league}{bot_config.football_url_path_calendar}"))

    actual_buttons_football = {**bot_config.buttons_football_leagues}  # new dict instance
    football_message_title = actual_buttons_football.pop(football_league)
    message = f"""<b>{football_message_title}</b>

    {get_football_data_message(matches)}"""
    sent_football_message(user, message, get_message_keyboard(actual_buttons_football, ParseMode.HTML))
