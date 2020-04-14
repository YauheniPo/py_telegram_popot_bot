# -*- coding: utf-8 -*-
import re
from datetime import datetime

from logger import logger

date_format_Y_m_d = '%Y-%m-%d'
date_format_iso = '%Y-%m-%dT%H:%M:%S'
date_format_d_m = '%d.%m'

json_data_regex = "{(.*)}"


def is_match_by_regexp(string, regexp):
    logger().info("String matching '{}'".format(string))
    pattern = re.compile(regexp)
    return bool(pattern.match(string))


def find_all_by_regexp(text, regexp):
    return re.findall(regexp, text)


def get_current_date():
    return datetime.date(datetime.now())
