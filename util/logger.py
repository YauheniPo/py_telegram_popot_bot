# -*- coding: utf-8 -*-
import logging.config
import sys
from os import path

from util import get_project_dirpath

LOGGING_CONFIG_FILE = "logging_config.ini"

log_file_path = path.join(get_project_dirpath(), LOGGING_CONFIG_FILE)
logging.config.fileConfig(log_file_path)


def logger():
    return logging.getLogger(sys._getframe(1).f_globals['__name__'])
