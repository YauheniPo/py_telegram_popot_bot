# -*- coding: utf-8 -*-
import logging.config
import sys

logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": 'DEBUG',
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "fileHandler": {
            "class": "logging.FileHandler",
            "filename": "log.log"
        }
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "fileHandler"]
        }
    }
})


def logger():
    return logging.getLogger(sys._getframe(1).f_globals['__name__'])
