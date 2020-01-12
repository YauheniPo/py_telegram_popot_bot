# -*- coding: utf-8 -*-
import logging

import requests

logger = logging.getLogger(__name__)


def get_site_request_content(url, params={}, cookies=None):
    logger.info("Get site content")
    r = requests.get(url, params=params, cookies=cookies)
    return r.text
