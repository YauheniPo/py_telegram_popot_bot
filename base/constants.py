# -*- coding: utf-8 -*-
import os

BASE_CMD_START = '/start'
BASE_CMD_CURRENCY = '/currency'
BASE_CMD_CINEMA = '/cinema'
BASE_CMD_FOOTBALL = '/football'
BASE_CMD_INSTAGRAM = '/instagram'
BASE_CMD_GEO = '/geo'
BASE_CMD_VIRUS = '/virus'

EMOJI_LOCATION = "📍"
EMOJI_CURRENCY = "💵"
EMOJI_ROBOT = "🤖"
EMOJI_CINEMA = "🎬"
EMOJI_PHOTO = "📷"
EMOJI_GRAPH = "📈"
EMOJI_FOOTBALL = "⚽"
EMOJI_FINGER_DOWN = "👇"

MSG_START_CMD_BASE = f"""
{EMOJI_ROBOT}    {BASE_CMD_START} - HELP - telegram bot functionals

{EMOJI_CURRENCY}    {BASE_CMD_CURRENCY} - $ / € / RUR - currency data and graph

{EMOJI_CINEMA}    {BASE_CMD_CINEMA} - cinema posters

{EMOJI_FOOTBALL}    {BASE_CMD_FOOTBALL} - football calendar

{EMOJI_PHOTO}    {BASE_CMD_INSTAGRAM} - save Instagram post content by link

{EMOJI_LOCATION}    {BASE_CMD_GEO} - location of the nearest ATMs

{EMOJI_GRAPH}    {BASE_CMD_VIRUS} - COVID-19 virus statistics"""

MSG_CURRENCY_BOT = """
<b>{currency}</b>
<i>{currency_past_days}</i>

<b>{currency_current_day}</b>"""

MSG_CURRENCY_ALARM_BOT = """
The last rate is <b>{today_rate}</b>

Please set your $ rate for notification.

<b>{around_today_rate}</b>"""

MSG_HTML_LINK = "<a href='{link}'>{title}</a>"

MSG_CINEMA_BOT = MSG_HTML_LINK + " <i>{media} | {info}</i>"

MSG_FOOTBALL_BASE_CMD = "Please select a section."
MSG_FOOTBALL_BOT = "<i>{date}</i>   <b>{host_team} -:- {guest_team}</b>"

MSG_INSTAGRAM_BOT = """
You will receive a post file from Instagram by sending a link to this post to the bot.

Please copy/share Instagram public post link and paste/move to bot."""
MSG_INSTAGRAM_POST_CONTENT = """<b>Post description:</b>
{}

<b>Post media:</b>
{}"""

MSG_LOCATION_MAP = """<a href='{link}'>GO to Yandex map.
Click here!</a>"""

MSG_VIRUS_COVID_DATA = """
{base_country_statistics}:
Cases: {world_cases_statistics}
Deaths: {world_deaths_statistics}
Recov: {world_recov_statistics}"""

DB_LOG_CMD = f"/{os.environ.get('LOG')}"
