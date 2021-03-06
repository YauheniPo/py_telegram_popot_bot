import os
import shutil

import pytest

from db.db_connection import get_db_json_data_path, DBConnector
from test.constants_test import TEST_ARCHIVE_FOLDER


@pytest.fixture(scope="session", autouse=True)
def remove_db_data_file():
    db_test_filename = get_db_json_data_path()
    os.remove(db_test_filename) if os.path.exists(db_test_filename) else None
    yield
    # Teardown


@pytest.fixture(scope="session", autouse=True)
def remove_test_archive():
    yield
    # Teardown
    test_archive_folder = TEST_ARCHIVE_FOLDER
    shutil.rmtree(test_archive_folder) if os.path.exists(
        test_archive_folder) else None


@pytest.fixture(scope='module')
def close_db_connection():
    yield
    # Teardown
    DBConnector().close()
