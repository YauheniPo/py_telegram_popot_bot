# -*- coding: utf-8 -*-
import os

from tinydb import TinyDB, Query

from logger import logger

db = TinyDB('db{}db.json'.format(os.path.sep))
users_table = db.table('users')
users = Query()


def get_db_user(user_id):
    db_users = users_table.search(users.id == user_id)
    return db_users[0] if db_users else []


def insert_user(user_data):
    logger().info("Insert user {}".format(user_data))
    users_table.insert({'id': user_data.id, 'username': user_data.username,
                        'first_name': user_data.first_name, 'last_name': user_data.last_name})
