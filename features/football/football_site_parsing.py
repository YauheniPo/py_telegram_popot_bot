import logging

from features.football.match import Match
from msg_context import football_bot_text

logger = logging.getLogger(__name__)


def get_matches(tree_matches):
    logger.info("Get matches")

    matches = []
    for match in tree_matches:
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
