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

        user = users_table.search(users.id == self.user_id)
        if not user:
            users_table.insert({'id': self.user_id, 'username': self.username,
                                'first_name': self.first_name, 'last_name': self.last_name})
        else:
            user[0]['username'] = self.username if user[0]['username'] is None else None
            user[0]['first_name'] = self.first_name if user[0]['first_name'] is None else None
            user[0]['last_name'] = self.last_name if user[0]['last_name'] is None else None
            users_table.write_back(user)

        logger.info(">>>>>>>>>--User--<<<<<<<<< " + str(self.__dict__))
