# -*- coding: utf-8 -*-


class User:

    def __init__(self, user_db):
        self.username = user_db['username']
        self.first_name = user_db['first_name']
        self.last_name = user_db['last_name']
        self.user_id = user_db['id']
