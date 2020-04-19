# -*- coding: utf-8 -*-
import json
from datetime import datetime

import pandas as pd
import requests
from lxml import html
from overload import overload
from systemtools import number

from bot_config import virus_covid_data_site_url, virus_covid_data_api_url, covid_graph_folder, covid_graph_path
from util.util_data import get_current_date
from util.util_graph import fetch_plot_graph_image
from util.util_request import get_site_request_content


def get_last_virus_covid_dir(location, table_data_xpath):
    covid_site_content = get_site_request_content(url=virus_covid_data_site_url)
    covid_tree_html_content = html.fromstring(covid_site_content)

    location_data = covid_tree_html_content.xpath(table_data_xpath)
    location_cases = number.parseNumber(location_data[-4].text_content().replace(',', ''))
    location_deaths = number.parseNumber(location_data[-3].text_content().replace(',', ''))
    location_recov = number.parseNumber(location_data[-2].text_content().replace(',', ''))
    return {'country': location,
            'dates': [str(get_current_date())],
            'cases': [location_cases],
            'deaths': [location_deaths],
            'recov.': [location_recov]}


@overload
def get_last_location_virus_covid_data_dir():
    return get_last_virus_covid_dir('World', "//tbody[.//*[@class='covid-sticky']]//th[@class]")


@get_last_location_virus_covid_data_dir.add
def get_last_virus_covid_data_dir(country: str):
    return get_last_virus_covid_dir(country, "//tr[.//a[@href][text()='{}']][.//img]/*".format(country))


def get_all_location_virus_covid_data_dir(country):
    response = requests.post(url=virus_covid_data_api_url, data=json.dumps({'country': country}))  # or {'code': 'BY'}

    # Convert to data frame
    df = pd.DataFrame.from_dict(json.loads(response.text))
    return {'country': country,
            'dates': df.date.values.tolist(),
            'cases': df.cases_cum.values.tolist(),
            'deaths': df.deaths_cum.values.tolist()}


def fetch_covid_graph(country_all_data_virus, country_actual_data_virus):
    if country_actual_data_virus['cases'][0] not in country_all_data_virus['cases']:
        country_all_data_virus['cases'].pop(0)
        country_all_data_virus['cases'].append(country_actual_data_virus['cases'][0])
    if country_actual_data_virus['deaths'][0] not in country_all_data_virus['deaths']:
        country_all_data_virus['deaths'].pop(0)
        country_all_data_virus['deaths'].append(country_actual_data_virus['deaths'][0])

    x_axis_dates = [datetime.strptime(date, '%Y-%m-%d') for date in country_all_data_virus['dates']]
    y_axis_cases = country_all_data_virus['cases']

    fetch_plot_graph_image(x_axis_dates, y_axis_cases, covid_graph_folder, covid_graph_path,
                           '{} for today ({})'.format(y_axis_cases[-1], x_axis_dates[-1].strftime("%d/%m/%Y")), 'o')


def get_covid_virus_msg_content(*args):
    msg_content = ["""{}:
Cases: {}
Deaths: {}
Recov: {}""".format(virus_data['country'], virus_data['cases'][0],
                    virus_data['deaths'][0], virus_data['recov.'][0]) for virus_data in args]
    return "\n\n".join(msg_content)

# matplotlib.use('Agg')
#
# covid19 = COVID19Py.COVID19(data_source="jhu")
# data = covid19.getLocationById(22)
# virus_details = dict(data["latest"])
# del virus_details['recovered']
# names = list(virus_details.keys())
# values = list(virus_details.values())
# plt.bar(range(len(virus_details)), values, tick_label=names)
# # for i in range(len(values)):
# # plt.annotate(s=str(values[0]), xy=(values[0], names[0]))
# if not os.path.exists(covid_graph_folder):
#     os.makedirs(covid_graph_folder)
# plt.savefig(covid_graph_path)
