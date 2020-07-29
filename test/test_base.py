# -*- coding: utf-8 -*-
import re
from os import path

from hamcrest import *

import popot_bot
from test.constants_test import ROBOT_SCRIPT_FUNC_NAME_REGEXP


def test_bot_script_func():
    bot_script_all = popot_bot.__all__
    with open(path.join(popot_bot.__file__), "r") as script:
        script_content = script.read()
    actual_bot_script_func = re.findall(
        ROBOT_SCRIPT_FUNC_NAME_REGEXP, script_content)
    assert_that(bot_script_all, contains_inanyorder(*actual_bot_script_func))
