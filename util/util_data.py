# -*- coding: utf-8 -*-
import re
from datetime import datetime

from util.logger import logger

DATE_FORMAT_Y_M_D = '%Y-%m-%d'
DATE_FORMAT_D_M_Y = '%d/%m/%Y'
DATE_FORMAT_ISO = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT_D_M = '%d.%m'


def is_match_by_regexp(string, regexp):
    logger().info("String matching '{}'".format(string))
    pattern = re.compile(regexp)
    return bool(pattern.match(string))


def find_all_by_regexp(text, regexp):
    return re.findall(regexp, text)


def get_current_date():
    return datetime.date(datetime.now())
