# -*- coding: utf-8 -*-
import logging.config
import sys

LOGGING_CONFIG_FILE = "logging_config.ini"

logging.config.fileConfig(LOGGING_CONFIG_FILE)


def logger():
    return logging.getLogger(sys._getframe(1).f_globals['__name__'])
