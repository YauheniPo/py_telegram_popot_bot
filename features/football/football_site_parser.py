# -*- coding: utf-8 -*-
from lxml import html

from bot_constants import MSG_FOOTBALL_BOT
from features.football.match import Match
from util.logger import logger


def get_matches(site_content):
    logger().info("Get matches")

    matches_tree_xpath = "//div[contains(@class, 'statistics-table')]//tr//td[contains(text(), '-:-')]/ancestor::tr"
    match_host_team_xpath = ".//div[contains(@class, 'team_left')]//span"
    match_guest_team_xpath = ".//div[contains(@class, 'team_right')]//span"
    match_date_xpath = ".//span[contains(@class, 'date') and contains(@class, 'desktop')]"

    matches = []

    xpath_get_text = "{xpath}//text()"
    for match in html.fromstring(site_content).xpath(matches_tree_xpath):
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
    return matches


def get_football_data_message(matches):
    return "\n".join([MSG_FOOTBALL_BOT.format(date=match.date,
                                              host_team=match.host_team,
                                              guest_team=match.guest_team) for match in matches])
