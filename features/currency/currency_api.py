# -*- coding: utf-8 -*-
import datetime

import requests

import bot_config
from base.constants import MSG_CURRENCY_BOT
from db.db_connection import DBConnector
from features.currency.сurrency import Currency
from util.logger import logger
from util.util_data import DATE_FORMAT_D_M, DATE_FORMAT_Y_M_D


def fetch_currency_list(json_data):
    return [Currency(**d) for d in json_data]


def get_currency_response_json(currency_id):
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)) \
        .strftime(DATE_FORMAT_Y_M_D)
    start_date = (
            datetime.datetime.now() -
            datetime.timedelta(
                days=bot_config.currency_graph_days)).strftime(DATE_FORMAT_Y_M_D)

    parameters = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.get(
        url="{currency_api_url}/{currency_id}".format(
            currency_api_url=bot_config.currency_api_url,
            currency_id=currency_id),
        params=parameters)

    return response.json()


def get_currency_data_message(currency_data_list):
    return "\n".join(
        ["{day} -    {rate} BYR".format(day=currency_day.Date.strftime(DATE_FORMAT_D_M),
                                        rate=currency_day.Cur_OfficialRate)
         for currency_day in currency_data_list])


def get_currency_message(currency_id):
    logger().info("Get currency data")

    currency_list = fetch_currency_list(
        get_currency_response_json(currency_id))

    currency_response_past_days = get_currency_data_message(
        currency_list[-10:-1])
    currency_response_current_day = get_currency_data_message(
        [currency_list[-1]])

    current_currency = bot_config.buttons_currency_selection[currency_id]
    return MSG_CURRENCY_BOT.format(
        currency=current_currency,
        currency_past_days=currency_response_past_days,
        currency_current_day=currency_response_current_day)


def get_currency_rate_list(currency_id):
    return fetch_currency_list(get_currency_response_json(currency_id))


def get_today_currency_rate():
    currency_list = get_currency_rate_list(bot_config.currency_dollar_id)
    return currency_list[-1].Cur_OfficialRate


def get_actual_currency_rate_for_alarm(user):
    db_user_alarm_currency_rate = DBConnector().get_db_user_alarm_currency_rate(user.user_id)
    today_currency_rate = get_today_currency_rate()
    if db_user_alarm_currency_rate:
        return today_currency_rate, db_user_alarm_currency_rate
    return today_currency_rate, today_currency_rate
