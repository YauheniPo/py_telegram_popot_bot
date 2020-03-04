# -*- coding: utf-8 -*-
import time

import schedule
from telegram import ParseMode

from base.user import get_user
from bot import bot
from features.currency.currency_api import get_currency_message
from features.instagram.insta_loader import *


def job():
    user = get_user(340648090)
    bot.send_message(chat_id=user.user_id,
                     text='<b>Currency Alarm</b>\n' + get_currency_message(currency_dollar_id),
                     parse_mode=ParseMode.HTML)


# schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
schedule.every().monday.thursday.wednesday.tuesday.friday.at("13:15").do(job)
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
