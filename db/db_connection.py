# -*- coding: utf-8 -*-
import json

from json2html import json2html
from tinydb import Query, TinyDB

from db import get_db_json_data_path
from util.logger import logger


DB_LOG_HTML = "popot_bot_log.html"


def fetch_log_table_html():
    db_log_data_str = DBConnector().get_db_all_data()
    db_log_data_html = json2html.convert(json=db_log_data_str)
    with open(DB_LOG_HTML, "w") as fp:
        fp.write(db_log_data_html)


class DBConnector(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.db_data_json_file = get_db_json_data_path()
        self.db = TinyDB(self.db_data_json_file)
        self.users_table = self.db.table('users')
        self.currency_alarm_table = self.db.table('currency_alarm')
        self.cmd_table = self.db.table('commands')
        # self.insta_followers_table = self.db.table('insta_followers')
        # self.user_insta_followers_table = self.db.table('user_insta_followers')
        self.query = Query()

    def close(self):
        self.db.close()

    def get_db_user(self, user_id):
        db_users = self.users_table.search(self.query.id == user_id)
        return db_users[0] if db_users else []

    def insert_user(self, user_chat):
        user_data = {
            'id': user_chat.id,
            'username': user_chat.username,
            'first_name': user_chat.first_name,
            'last_name': user_chat.last_name}
        self.users_table.insert(user_data)
        logger().info("Insert user {}".format(user_data))

    def insert_analytics(self, user, cmd):
        logger().info("Insert analytics command '{}' of user {}".format(cmd, user.__dict__))
        user_db_analytics = self.cmd_table.search(
            self.query.id == user.user_id)
        if user_db_analytics:
            user_db_cmd_analytics = self.cmd_table.search(
                (self.query.id == user.user_id) & (self.query[cmd]))
            if user_db_cmd_analytics:
                user_db_cmd_analytics[0][cmd] += 1
                self.cmd_table.write_back(user_db_cmd_analytics)
            else:
                user_db_analytics[0][cmd] = 1
                self.cmd_table.write_back(user_db_analytics)
        else:
            self.cmd_table.insert({'id': user.user_id, cmd: 1})

    def get_db_user_alarm_currency_rate(self, user_id):
        db_user_alarm_currency_rate = self.currency_alarm_table.search(
            self.query.id == user_id)
        return db_user_alarm_currency_rate[0]['alarm_rate'] if db_user_alarm_currency_rate else [
        ]

    def get_db_users_alarm_currency_rate(self):
        return self.currency_alarm_table.all()

    def insert_currency_alarm(self, user, alarm_rate):
        logger().info(
            "Insert analytics currency rate alarm '{}' of user {}".format(
                alarm_rate, user.__dict__))
        user_db_analytics = self.currency_alarm_table.search(
            self.query.id == user.user_id)
        if user_db_analytics:
            user_db_analytics[0]['alarm_rate'] = alarm_rate
            self.currency_alarm_table.write_back(user_db_analytics)
        else:
            self.currency_alarm_table.insert(
                {'id': user.user_id, 'alarm_rate': alarm_rate})

    def get_db_all_data(self):
        with open(self.db_data_json_file, "rb") as fp:
            return json.load(fp)
