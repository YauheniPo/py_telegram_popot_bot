# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class User:

    def __init__(self, message):
        self.last_name = message.from_user.last_name
        self.first_name = message.from_user.first_name
        self.username = message.from_user.username
        self.user_id = message.from_user.id
        self.lang = message.from_user.language_code
        self.message_text = message.text
        self.message = message
        logger.info(str(self.__dict__))

    def __repr__(self):
        return str(self.__dict__)
