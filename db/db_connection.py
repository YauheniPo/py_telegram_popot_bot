# -*- coding: utf-8 -*-
import os

from tinydb import TinyDB, Query

from logger import logger

db = TinyDB('db{}db.json'.format(os.path.sep))
users_table = db.table('users')
cmd_table = db.table('commands')
currency_alarm_table = db.table('currency_alarm')
query = Query()


def get_db_user(user_id):
    db_users = users_table.search(query.id == user_id)
    return db_users[0] if db_users else []


def insert_user(user):
    logger().info("Insert user {}".format(user))
    users_table.insert({'id': user.user_id, 'username': user.username,
                        'first_name': user.first_name, 'last_name': user.last_name})


def insert_analytics(user, cmd):
    logger().info("Insert analytics command '{}' of user {}".format(cmd, user.__dict__))
    user_db_analytics = cmd_table.search(query.id == user.user_id)
    if user_db_analytics:
        user_db_cmd_analytics = cmd_table.search((query.id == user.user_id) & (query[cmd]))
        if user_db_cmd_analytics:
            user_db_cmd_analytics[0][cmd] += 1
            cmd_table.write_back(user_db_cmd_analytics)
        else:
            user_db_analytics[0][cmd] = 1
            cmd_table.write_back(user_db_analytics)
    else:
        cmd_table.insert({'id': user.user_id, cmd: 1})
