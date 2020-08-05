# -*- coding: utf-8 -*-
import pytest
from hamcrest import assert_that, is_, equal_to, is_not, empty
from simpledate import SimpleDate

import bot_config
from features.football.football_site_parser import get_matches
from features.instagram.insta_loader import fetch_insta_post_data
from features.instagram.insta_post import InstaPost
from test.constants_test import INSTAGRAM_PUBLIC_POST_LINK, INSTAGRAM_PRIVATE_POST_LINK
from util.util_request import get_site_request_content


@pytest.mark.parametrize(
    "insta_post",
    [pytest.param(InstaPost(post_url=INSTAGRAM_PUBLIC_POST_LINK),
                  marks=pytest.mark.xfail(SimpleDate().tzinfo == 'Etc/UTC',
                                          reason="Instagram post from private account.")),
     pytest.param(InstaPost(post_url=INSTAGRAM_PRIVATE_POST_LINK),
                  marks=pytest.mark.xfail(reason="Instagram post from private account."))],
    ids=["Instagram public post.",
         "Instagram private post."])
def test_insta_post_fetching_data(insta_post):
    """Test of fetching Instagram post data."""

    fetch_insta_post_data(insta_post)

    assert_that(len(insta_post.media_urls) > 1, is_(equal_to(
        True)), f"Media from Instagram post {insta_post.__dict__} fetched incorrect.")
    assert_that(
        insta_post.post_description,
        is_not(
            empty()),
        f"Description from Instagram post {insta_post.__dict__} fetched incorrect.")


@pytest.mark.parametrize(
    "league",
    [bot_config.football_ucl_path,
     bot_config.football_le_path],
    ids=["UEFA Champions League.",
         "UEFA Europa League."]
)
def test_football_league(league):
    """Test of fetching football league calendar."""

    matches = get_matches(get_site_request_content(
        url=f"{bot_config.football_url}{league}{bot_config.football_url_path_calendar}"))

    assert_that(
        matches,
        is_not(
            empty()),
        f"Description from Instagram post {matches} fetched incorrect.")
