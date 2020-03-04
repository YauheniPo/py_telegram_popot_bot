# -*- coding: utf-8 -*-
import time

import schedule
from telegram import ParseMode

from bot import bot
from db.db_connection import get_users_alarm_currency_rate
from features.currency.currency_api import get_currency_message, fetch_currency_list, get_currency_response_json
from features.instagram.insta_loader import *
from util.bot_helper import get_message_keyboard


def job():
    users = get_users_alarm_currency_rate()
    for user in users:
        currency_list = fetch_currency_list(get_currency_response_json(currency_dollar_id))
        today_currency_rate = currency_list[-1].Cur_OfficialRate

        if today_currency_rate >= user['alarm_rate']:
            actual_buttons_currency_selection = dict(buttons_currency_selection)
            del actual_buttons_currency_selection[currency_dollar_id]

            bot.send_message(chat_id=user['id'],
                             text='<b>Currency Alarm</b>\n' + get_currency_message(currency_dollar_id),
                             reply_markup=get_message_keyboard(button_currency_graph, actual_buttons_currency_selection, button_currency_alarm),
                             parse_mode=ParseMode.HTML)


schedule.every(12).seconds.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().monday.thursday.wednesday.tuesday.friday.at("12:05").do(job)
# schedule.every().minute.at(":17").do(job)

if __name__ == "__main__":
    for i in range(0, 5):
        time.sleep(60)
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except Exception as e:
            logger().error(e)
