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
        "{currency_api_url}{currency_id}".format(currency_api_url=config.currency_api_url,
                                                 currency_id=config.dollar_id),
        params=parameters)

    return response.json()
