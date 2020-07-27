from telegram import ParseMode

import bot_config
from base.bot.bot import bot
from features.football.football_site_parser import get_matches, get_football_data_message
from util.bot_helper import get_message_keyboard
from util.util_request import get_site_request_content


def send_football_calendar(user, football_league):
    matches = get_matches(
        get_site_request_content(
            url=bot_config.football_url +
                football_league +
                bot_config.football_url_path_calendar))

    actual_buttons_football = dict(bot_config.buttons_football_leagues)
    football_message_title = actual_buttons_football.pop(football_league)

    bot.send_message(
        chat_id=user.user_id,
        text="<b>{}</b>\n\n".format(football_message_title) +
             get_football_data_message(matches),
        reply_markup=get_message_keyboard(actual_buttons_football),
        parse_mode=ParseMode.HTML)
