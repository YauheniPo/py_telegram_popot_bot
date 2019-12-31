# -*- coding: utf-8 -*-
import datetime

import requests

import config
from features.currency.сurrency import Currency


def fetch_currency_list(json_data):
    return [Currency(**d) for d in json_data]


def get_currency_response_json():
    import util.util_date as date_util
    end_date = datetime.datetime.now().strftime(date_util.currency_api_param_date_format)
    start_date = (datetime.datetime.now() - datetime.timedelta(days=config.currency_graph_days)).strftime(
        date_util.currency_api_param_date_format)

    parameters = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.get(
        url="{currency_api_url}{currency_id}".format(currency_api_url=config.currency_api_url,
                                                     currency_id=config.currency_dollar_id),
        params=parameters)

    return response.json()


def get_currency_data_message(currency_data_list, currency_msg_date_format):
    return "\n".join(
        ["{day} -    {rate} BYR".format(day=currency_day.Date.strftime(currency_msg_date_format),
                                        rate=currency_day.Cur_OfficialRate)
         for currency_day in currency_data_list])
