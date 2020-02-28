# -*- coding: utf-8 -*-
from db.db_connection import get_db_user, insert_user
from logger import logger


class User:

    def __init__(self, user_db):
        self.username = user_db['username']
        self.first_name = user_db['first_name']
        self.last_name = user_db['last_name']
        self.user_id = user_db['id']


def get_user(user_id):
    user_db = get_db_user(user_id=user_id)
    logger().info("***** {} *****".format(user_db))
    return User(user_db=user_db)


def fetch_user(chat):
    user = get_db_user(chat.id)
    if not user:
        insert_user(chat)
    return get_user(user_id=chat.id)
