# -*- coding: utf-8 -*-
import datetime
import logging

import requests

import config
from features.currency.сurrency import Currency
from util.util_parsing import date_format_d_m, date_format_Y_m_d

logger = logging.getLogger(__name__)


def fetch_currency_list(json_data):
    return [Currency(**d) for d in json_data]


def get_currency_response_json(currency_id):
    logger.info("Get currency data")

    end_date = datetime.datetime.now().strftime(date_format_Y_m_d)
    start_date = (datetime.datetime.now() - datetime.timedelta(days=config.currency_graph_days)) \
        .strftime(date_format_Y_m_d)

    parameters = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.get(
        url="{currency_api_url}/{currency_id}".format(currency_api_url=config.currency_api_url,
                                                      currency_id=currency_id),
        params=parameters)

    return response.json()


def get_currency_data_message(currency_data_list):
    return "\n".join(
        ["{day} -    {rate} BYR".format(day=currency_day.Date.strftime(date_format_d_m),
                                        rate=currency_day.Cur_OfficialRate)
         for currency_day in currency_data_list])
