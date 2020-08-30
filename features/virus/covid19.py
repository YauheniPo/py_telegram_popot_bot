# -*- coding: utf-8 -*-
import json
from datetime import datetime

import pandas as pd
import requests
from lxml import html
from overload import overload
from systemtools import number

from base.constants import MSG_VIRUS_COVID_DATA
from bot_config import virus_covid_data_api_url, covid_graph_path, \
    virus_covid_data_wikipedia_site_url
from util.util_data import get_current_date, DATE_FORMAT_D_M_Y, DATE_FORMAT_Y_M_D
from util.util_graph import fetch_plot_graph_image
from util.util_request import get_site_request_content


def get_tutby_last_virus_covid_dir(location, covid_all_data):
    return {'country': location.upper(),
            'dates': [str(get_current_date())],
            'cases': [covid_all_data['cases'][-1]],
            'deaths': [covid_all_data['deaths'][-1]]}


def get_last_virus_covid_dir(location, table_data_xpath):
    covid_site_content = get_site_request_content(
        url=virus_covid_data_wikipedia_site_url)
    covid_tree_html_content = html.fromstring(covid_site_content)

    location_data = covid_tree_html_content.xpath(table_data_xpath)
    location_cases = number.parseNumber(
        location_data[-4].text_content().replace(',', ''))
    location_deaths = number.parseNumber(
        location_data[-3].text_content().replace(',', ''))
    return {'country': location.upper(),
            'dates': [str(get_current_date())],
            'cases': [location_cases],
            'deaths': [location_deaths]}


@overload
def get_last_virus_covid_data_dir():
    return get_last_virus_covid_dir(
        'World', "//tbody[.//*[@class='covid-sticky']]//tr[@class='sorttop']/th")


@get_last_virus_covid_data_dir.add
def get_last_virus_covid_data_dir(country: str, covid_all_data: dict):
    return get_tutby_last_virus_covid_dir(country, covid_all_data)


def get_location_all_virus_covid_data_dir(country):
    response = requests.post(url=virus_covid_data_api_url, data=json.dumps(
        {'country': country}))  # or {'code': 'BY'}

    # Convert to data frame
    df = pd.DataFrame.from_dict(json.loads(response.text))
    return {'country': country,
            'dates': df.date.values.tolist(),
            'cases': df.cases_cum.values.tolist(),
            'deaths': df.deaths_cum.values.tolist()}


def fetch_covid_graph(country_all_data_virus, country_actual_data_virus):
    if country_actual_data_virus['cases'][0] not in country_all_data_virus['cases']:
        country_all_data_virus['cases'].pop(0)
        country_all_data_virus['cases'].append(
            country_actual_data_virus['cases'][0])
    if country_actual_data_virus['deaths'][0] not in country_all_data_virus['deaths']:
        country_all_data_virus['deaths'].pop(0)
        country_all_data_virus['deaths'].append(
            country_actual_data_virus['deaths'][0])

    country_per_day_cases = []
    for index in range(1, len(country_all_data_virus['cases'])):
        country_per_day_cases.append(
            country_all_data_virus['cases'][index] - country_all_data_virus['cases'][index - 1])

    x_axis_dates = [datetime.strptime(date, DATE_FORMAT_Y_M_D)
                    for date in country_all_data_virus['dates']][-120:]
    y_axis_total_cases = country_all_data_virus['cases'][-120:]
    y_axis_cases_per_day = country_per_day_cases[-120:]

    fetch_plot_graph_image(x_axis_dates,
                           [y_axis_total_cases, y_axis_cases_per_day],
                           covid_graph_path,
                           ['{} today ({})'.format(y_axis_total_cases[-1],
                                                   x_axis_dates[-1].strftime(DATE_FORMAT_D_M_Y)),
                            '{} for today ({})'.format(y_axis_cases_per_day[-1],
                                                       x_axis_dates[-1].strftime(DATE_FORMAT_D_M_Y))],
                           ['total cases', 'cases per day'],
                           ['blue', 'red'],
                           ['o', 'r-'])


def get_covid_virus_msg_content(*args):
    msg_content = [
        MSG_VIRUS_COVID_DATA.format(
            base_country_statistics=virus_data['country'],
            world_cases_statistics=virus_data['cases'][0],
            world_deaths_statistics=virus_data['deaths'][0]) for virus_data in args]
    return "\n".join(msg_content)
