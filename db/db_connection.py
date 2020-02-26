# -*- coding: utf-8 -*-
import os

from tinydb import TinyDB, Query

db = TinyDB('db{}db.json'.format(os.path.sep))
users_table = db.table('users')
users = Query()
