# -*- coding: utf-8 -*-
import logging
import config
import requests

logger = logging.getLogger(__name__)


def get_site_content(url, params={}):
    logger.info("Get site content")

    r = requests.get(config.uri_https.format(url=url), params=params)
    return r.text
