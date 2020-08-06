# -*- coding: utf-8 -*-
import os
import random
import re
from datetime import datetime
from os import path

import pytest
from hamcrest import *
from hamcrest.core.core import is_
from telegram import Chat

import popot_bot
from base.models.user import User
from test.constants_test import ROBOT_SCRIPT_FUNC_NAME_REGEXP, TEST_ARCHIVE_FOLDER, TEST_GRAPH_IMAGE_PNG_NAME
from util.util_graph import fetch_plot_graph_image
from util.webdriver_helper import FIREFOX, CHROME, WebDriverFactory


def test_bot_script_func():
    """Test for full compliance of the functions of the base class and those declared in the __all__."""

    bot_script_all = popot_bot.__all__
    with open(path.join(popot_bot.__file__), "r") as script:
        script_content = script.read()
    actual_bot_script_func = re.findall(
        ROBOT_SCRIPT_FUNC_NAME_REGEXP, script_content)

    assert_that(
        bot_script_all,
        contains_inanyorder(
            *
            actual_bot_script_func),
        reason=f"Functions from bot base script '{popot_bot.__name__}' does not compliance with '__all__' data.")


@pytest.mark.parametrize(
    "user_chat_mock",
    [Chat(id=random.randrange(10, 1000), type=None, username="test_username",
          first_name="test_first_name", last_name="test_last_name"),
     Chat(id=random.randrange(10, 1000), type=None)],
    ids=["valid_user_with_all_data",
         "valid_user_with_only_id"]
)
def test_db_user_fetching(user_chat_mock, close_db_connection):
    """Test for checking user data obtained from the DB."""

    user_from_db = User.fetch_user(user_chat_mock)

    assert_that(user_from_db.user_id,
                is_(user_chat_mock.id),
                "Users ID is invalid from DB.")
    assert_that(user_from_db.username,
                is_(user_chat_mock.username),
                "Users username is invalid from DB.")
    assert_that(user_from_db.first_name,
                is_(user_chat_mock.first_name),
                "Users first name is invalid from DB.")
    assert_that(user_from_db.last_name,
                is_(user_chat_mock.last_name),
                "Users last name is invalid from DB.")


@pytest.mark.parametrize(
    "browser",
    [FIREFOX,
     CHROME],
    ids=[FIREFOX,
         CHROME]
)
def test_webdriver_instance(browser):
    """Test of checking valid initialization browser instance."""

    with WebDriverFactory(browser).get_webdriver_instance() as driver:
        assert_that(
            driver,
            not_none(),
            f"WebDriver of {browser} does not initialize.")


def test_plot_graph_image_generation():
    """Test of generation graph image."""

    test_graph_image_path = os.path.join(
        TEST_ARCHIVE_FOLDER, TEST_GRAPH_IMAGE_PNG_NAME)
    fetch_plot_graph_image([datetime.now()], [random.randrange(10, 1000)],
                           test_graph_image_path, "test_label")

    assert_that(os.path.exists(test_graph_image_path), is_(equal_to(True)),
                f"Graph image '{test_graph_image_path}' does not generate.")
