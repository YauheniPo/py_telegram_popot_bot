# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class User:

    def __init__(self, chat=None, user_id=None):
        if user_id is None:
            self.last_name = chat.last_name
            self.first_name = chat.first_name
            self.username = chat.username
            self.user_id = chat.id
        else:
            self.user_id = user_id

        logger.info(str(self.__dict__))

    def __repr__(self):
        return "--User-- " + str(self.__dict__)
