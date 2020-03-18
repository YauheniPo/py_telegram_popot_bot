# -*- coding: utf-8 -*-
import re

from lxml import html

from logger import logger

date_format_Y_m_d = '%Y-%m-%d'
date_format_iso = '%Y-%m-%dT%H:%M:%S'
date_format_d_m = '%d.%m'

json_data_regex = "{(.*)}"


def get_tree_html_content(site_content):
    return html.fromstring(site_content)


def find_elements(site_content, xpath):
    return get_tree_html_content(site_content).xpath(xpath)


def is_match_by_regexp(string, regexp):
    logger().info("String matching '{}'".format(string))
    pattern = re.compile(regexp)
    return bool(pattern.match(string))


def find_all_by_regexp(text, regexp):
    return re.findall(regexp, text)
