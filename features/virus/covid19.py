# -*- coding: utf-8 -*-
import json

import pandas as pd
import requests

from bot_config import virus_covid_data_site_url, virus_covid_data_api_url
from logger import logger
from util.util_parsing import get_tree_html_content
from util.util_request import get_site_request_content


covid_site_content = get_site_request_content(url=virus_covid_data_site_url)
covid_tree_html_content = get_tree_html_content(covid_site_content)


def fetch_covid_graph(virus_data):
    pass


def get_last_world_virus_covid_data_dir():
    pass


def get_last_virus_covid_data_dir(country):
    logger().info("Get matches")

    matches_tree_xpath = "//div[contains(@class, 'statistics-table')]//tr//td[contains(text(), '-:-')]/ancestor::tr"
    match_host_team_xpath = ".//div[contains(@class, 'team_left')]//span"
    match_guest_team_xpath = ".//div[contains(@class, 'team_right')]//span"
    match_date_xpath = ".//span[contains(@class, 'date') and contains(@class, 'desktop')]"

    matches = []

    xpath_get_text = "{xpath}//text()"
    for match in get_tree_html_content(site_content).xpath(matches_tree_xpath):
        match_host_team = match.xpath(
            xpath_get_text.format(
                xpath=match_host_team_xpath))[0]
        match_guest_team = match.xpath(
            xpath_get_text.format(
                xpath=match_guest_team_xpath))[0]
        match_date = str(
            match.xpath(
                xpath_get_text.format(
                    xpath=match_date_xpath))[0]).strip()
        matches.append(
            Match(
                host_team=match_host_team,
                guest_team=match_guest_team,
                date=match_date))
    return {'country': '', 'dates': [], 'cases': [], 'deaths': [], 'recov.': []}


def get_all_virus_covid_data_dir(country):
    response = requests.post(url=virus_covid_data_api_url, data=json.dumps({'country': country})) # or {'code': 'BY'}

    # Convert to data frame
    df = pd.DataFrame.from_dict(json.loads(response.text))
    return {'country': '', 'dates': [], 'cases': [], 'deaths': [], 'recov.': []}


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
