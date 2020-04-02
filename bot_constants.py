# -*- coding: utf-8 -*-
import os

BASE_CMD_START = '/start'
BASE_CMD_CURRENCY = '/currency'
BASE_CMD_CINEMA = '/cinema'
BASE_CMD_FOOTBALL = '/football'
BASE_CMD_INSTAGRAM = '/instagram'
BASE_CMD_GEO = '/geo'

MSG_START_CMD_BASE = """
{start} - HELP - telegram bot functionals
{currency} - $ / € / RUR - currency data and graph
{cinema} - cinema posters
{football} - football calendar
{instagram} - save Instagram post content by link
{geo} - location of the nearest ATMs"""

MSG_CURRENCY_BOT = """
<b>{currency}</b>
<i>{currency_past_days}</i>

<b>{currency_current_day}</b>"""

MSG_CURRENCY_ALARM_BOT = """The last rate is <b>{today_rate}</b>

Please set your $ rate for notification.

<b>{around_today_rate}</b>"""

MSG_SUCCESS = "Success!"
MSG_HTML_LINK = "<a href='{link}'>{title}</a>"

MSG_CINEMA_BOT = MSG_HTML_LINK + " <i>{media} | {info}</i>"

MSG_FOOTBALL_BASE_CMD = "Please select a section."
MSG_FOOTBALL_BOT = "<i>{date}</i>   <b>{host_team} -:- {guest_team}</b>"

MSG_INSTAGRAM_BOT = """
You will receive a post file from Instagram by sending a link to this post to the bot.

Please copy/share Instagram post link and paste/move to bot."""
MSG_INSTAGRAM_POST_CONTENT = "<b>Post description:</b>\n{}\n\n<b>Post media:</b>\n{}"

MSG_LOCATION_MAP = "<a href='{link}'>GO to Yandex map.\nClick here!</a>"

DB_LOG_CMD = '/{}'.format(os.environ.get('LOG'))
