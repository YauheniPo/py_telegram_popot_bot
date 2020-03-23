# -*- coding: utf-8 -*-
import json
import os

from tinydb import Query, TinyDB

from logger import logger

db_data_json_file = 'db{}db.json'.format(os.path.sep)
db = TinyDB(db_data_json_file)
users_table = db.table('users')
cmd_table = db.table('commands')
currency_alarm_table = db.table('currency_alarm')
query = Query()


def get_db_user(user_id):
    db_users = users_table.search(query.id == user_id)
    return db_users[0] if db_users else []


def insert_user(user_chat):
    user_data = {
        'id': user_chat.id,
        'username': user_chat.username,
        'first_name': user_chat.first_name,
        'last_name': user_chat.last_name}
    users_table.insert(user_data)
    logger().info("Insert user {}".format(user_data))


def insert_analytics(user, cmd):
    logger().info("Insert analytics command '{}' of user {}".format(cmd, user.__dict__))
    user_db_analytics = cmd_table.search(query.id == user.user_id)
    if user_db_analytics:
        user_db_cmd_analytics = cmd_table.search(
            (query.id == user.user_id) & (query[cmd]))
        if user_db_cmd_analytics:
            user_db_cmd_analytics[0][cmd] += 1
            cmd_table.write_back(user_db_cmd_analytics)
        else:
            user_db_analytics[0][cmd] = 1
            cmd_table.write_back(user_db_analytics)
    else:
        cmd_table.insert({'id': user.user_id, cmd: 1})


def get_users_alarm_currency_rate():
    return currency_alarm_table.all()


def insert_currency_alarm(user, alarm_rate):
    logger().info(
        "Insert analytics currency rate alarm '{}' of user {}".format(
            alarm_rate, user.__dict__))
    user_db_analytics = currency_alarm_table.search(query.id == user.user_id)
    if user_db_analytics:
        user_db_analytics[0]['alarm_rate'] = alarm_rate
        currency_alarm_table.write_back(user_db_analytics)
    else:
        currency_alarm_table.insert(
            {'id': user.user_id, 'alarm_rate': alarm_rate})


def get_db_data():
    with open(db_data_json_file, "rb") as fin:
        return json.load(fin)
