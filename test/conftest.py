import os

import pytest

from db.db_connection import get_db_json_data_path


@pytest.fixture(scope="session", autouse=True)
def remove_db_data_file():
    yield
    # Teardown
    db_test_filename = get_db_json_data_path()
    os.remove(db_test_filename) if os.path.exists(db_test_filename) else None
