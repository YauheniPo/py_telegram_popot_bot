# -*- coding: utf-8 -*-
import time

import schedule
from telegram import ParseMode

import bot_config
from base.bot.bot import bot
from db.db_connection import get_users_alarm_currency_rate
from features.currency.currency_api import (fetch_currency_list,
                                            get_currency_message,
                                            get_currency_response_json)
from util.bot_helper import get_message_keyboard
from util.logger import logger


def job():
    users = get_users_alarm_currency_rate()
    for user in users:
        currency_list = fetch_currency_list(
            get_currency_response_json(bot_config.currency_dollar_id))
        today_currency_rate = currency_list[-1].Cur_OfficialRate

        if today_currency_rate >= user['alarm_rate']:
            actual_buttons_currency_selection = dict(
                bot_config.buttons_currency_selection)
            del actual_buttons_currency_selection[bot_config.currency_dollar_id]

            bot.send_message(
                chat_id=user['id'],
                text=f"""
<b>Currency Alarm</b>
{get_currency_message(bot_config.currency_dollar_id)}""",
                reply_markup=get_message_keyboard(
                    bot_config.button_currency_graph,
                    actual_buttons_currency_selection,
                    bot_config.button_currency_alarm),
                parse_mode=ParseMode.HTML)


for schedule_time in ["12:39"]:
    schedule.every().monday.at(schedule_time).do(job, schedule_time)
    schedule.every().tuesday.at(schedule_time).do(job, schedule_time)
    schedule.every().wednesday.at(schedule_time).do(job, schedule_time)
    schedule.every().thursday.at(schedule_time).do(job, schedule_time)
    schedule.every().friday.at(schedule_time).do(job, schedule_time)

if __name__ == "__main__":
    for i in range(0, 5):
        time.sleep(20)
        try:
            while True:
                schedule.run_pending()
                time.sleep(15)
        except Exception as e:
            logger().error(e)
