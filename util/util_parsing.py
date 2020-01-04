# -*- coding: utf-8 -*-
import logging
import re

from lxml import html

logger = logging.getLogger(__name__)


def get_tree_html_content(site_content):
    return html.fromstring(site_content)


def is_match_by_regexp(string, regexp):
    logger.info("String matching '{}'".format(string))
    pattern = re.compile(regexp)
    return bool(pattern.match(string))
