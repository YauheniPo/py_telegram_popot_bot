# -*- coding: utf-8 -*-
import logging
import re

from lxml import html

logger = logging.getLogger(__name__)

date_format_Y_m_d = '%Y-%m-%d'
date_format_iso = '%Y-%m-%dT%H:%M:%S'
date_format_d_m = '%d.%m'

json_data_regex = "{(.*)}"


def get_tree_html_content(site_content):
    return html.fromstring(site_content)


def is_match_by_regexp(string, regexp):
    logger.info("String matching '{}'".format(string))
    pattern = re.compile(regexp)
    return bool(pattern.match(string))
