# -*- coding: utf-8 -*-
import random
import re
from os import path

import pytest
from hamcrest import *
from hamcrest.core.core import is_
from telegram import Chat

import popot_bot
from base.models.user import User
from test.constants_test import ROBOT_SCRIPT_FUNC_NAME_REGEXP


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
def test_db_user_fetching(user_chat_mock):
    """."""
    user_from_db = User.fetch_user(user_chat_mock)

    assert_that(user_from_db.user_id, is_(user_chat_mock.id))
    assert_that(user_from_db.username, is_(user_chat_mock.username))
    assert_that(user_from_db.first_name, is_(user_chat_mock.first_name))
    assert_that(user_from_db.last_name, is_(user_chat_mock.last_name))
