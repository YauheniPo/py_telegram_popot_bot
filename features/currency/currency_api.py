# -*- coding: utf-8 -*-
import datetime

import requests

import bot_config
from bot_constants import MSG_CURRENCY_BOT
from features.currency.сurrency import Currency
from logger import logger
from util.util_parsing import date_format_d_m, date_format_Y_m_d


def fetch_currency_list(json_data):
    return [Currency(**d) for d in json_data]


def get_currency_response_json(currency_id):
    end_date = datetime.datetime.now().strftime(date_format_Y_m_d)
    start_date = (datetime.datetime.now() - datetime.timedelta(days=bot_config.currency_graph_days)) \
        .strftime(date_format_Y_m_d)

    parameters = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.get(
        url="{currency_api_url}/{currency_id}".format(currency_api_url=bot_config.currency_api_url,
                                                      currency_id=currency_id),
        params=parameters)

    return response.json()


def get_currency_data_message(currency_data_list):
    return "\n".join(
        ["{day} -    {rate} BYR".format(day=currency_day.Date.strftime(date_format_d_m),
                                        rate=currency_day.Cur_OfficialRate)
         for currency_day in currency_data_list])


def get_currency_message(currency_id):
    logger().info("Get currency data")

    currency_list = fetch_currency_list(get_currency_response_json(currency_id))

    currency_response_past_days = get_currency_data_message(currency_list[-10:-1])
    currency_response_current_day = get_currency_data_message([currency_list[-1]])

    current_currency = bot_config.buttons_currency_selection[currency_id]
    return MSG_CURRENCY_BOT.format(
        currency=current_currency,
        currency_past_days=currency_response_past_days,
        currency_current_day=currency_response_current_day)
