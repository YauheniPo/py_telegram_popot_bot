# -*- coding: utf-8 -*-
from telegram import Chat

from db.db_connection import DBConnector
from util.logger import logger


class User:

    def __init__(self, user_db):
        self.username = user_db['username']
        self.first_name = user_db['first_name']
        self.last_name = user_db['last_name']
        self.user_id: int = user_db['id']

    @classmethod
    def get_user(cls, user_id):
        user_db = DBConnector().get_db_user(user_id=user_id)
        logger().info(f"***** {user_db} *****")
        return cls(user_db=user_db)

    @staticmethod
    def fetch_user(chat: Chat):
        user = DBConnector().get_db_user(chat.id)
        if not user:
            DBConnector().insert_user(chat)
        return User.get_user(user_id=chat.id)
