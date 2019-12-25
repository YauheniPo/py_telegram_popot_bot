import json

import requests
import datetime

from features.currency.сurrency import Currency

dollar_id = 145
date_format = "%Y-%m-%d"


def fetch_currency_list(json_data):
    return [Currency(**d) for d in json_data]


def get_currency_response_json():
    end_date = datetime.datetime.now().strftime(date_format)
    start_date = (datetime.datetime.now() - datetime.timedelta(days=300)).strftime(date_format)

    parameters = {
        "startDate": start_date,
        "endDate": end_date
    }

    response = requests.get("http://www.nbrb.by/API/ExRates/Rates/Dynamics/{currency_id}".format(currency_id=dollar_id),
                            params=parameters)

    return response.json()