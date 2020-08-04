import os
from os import path

from util import get_project_dirpath

JSON_EXTENSION = ".json"
DB_FILENAME = "db_bot"


def get_db_json_data_path(db_json=os.environ.get('DB_TEST', DB_FILENAME)):
    return path.join(get_project_dirpath(), "db", db_json + JSON_EXTENSION)
