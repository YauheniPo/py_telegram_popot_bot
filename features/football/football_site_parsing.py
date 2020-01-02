# -*- coding: utf-8 -*-
import logging

from features.football.match import Match
from msg_context import football_bot_text
from util.util_parsing import get_tree_html_content

logger = logging.getLogger(__name__)


def get_matches(site_content):
    logger.info("Get matches")

    matches = []
    for match in get_tree_html_content(site_content).xpath(
            "//div[contains(@class, 'statistics-table')]//tr//td[contains(text(), '-:-')]/ancestor::tr"):
        host_team = match.xpath(".//div[contains(@class, 'team_left')]//span//text()")[0]
        guest_team = match.xpath(".//div[contains(@class, 'team_right')]//span//text()")[0]
        match_date = \
            str(match.xpath(".//span[contains(@class, 'date') and contains(@class, 'desktop')]//text()")[0]).strip()
        matches.append(Match(host_team=host_team, guest_team=guest_team, date=match_date))
    return matches


def get_football_data_message(matches):
    return "\n".join(
        [football_bot_text.format(date=match.date, host_team=match.host_team, guest_team=match.guest_team)
         for match in matches])
