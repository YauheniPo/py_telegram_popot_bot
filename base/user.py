# -*- coding: utf-8 -*-
import logging

from popot_bot import users_table, users

logger = logging.getLogger(__name__)


class User:
    username: str = None
    first_name: str = None
    last_name: str = None

    def __init__(self, chat=None, user_id=None):
        if user_id is None:
            self.username = chat.username
            self.first_name = chat.first_name
            self.last_name = chat.last_name
            self.user_id = chat.id
        else:
            self.user_id = user_id

        if not users_table.search(users.id == self.user_id):
            users_table.insert({'id': self.user_id, 'username': self.username,
                                'first_name': self.first_name, 'last_name': self.last_name})

        logger.info(">>>>>>>>>--User--<<<<<<<<< " + str(self.__dict__))
