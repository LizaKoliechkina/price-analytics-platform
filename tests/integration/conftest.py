import os

import pytest
from loguru import logger
from sqlalchemy import create_engine, text

API_URL = os.environ.get('API_URL')
TEST_DB_URL = os.environ.get('TEST_DB_URL')


@pytest.fixture(scope='module')
def clean_up_test_objects():
    test_db = create_engine(TEST_DB_URL)
    conn = test_db.connect()
    logger.debug('Database ready for cleanup after tests run.')
    yield
    logger.debug('Start cleaning up test objects...')
    conn.execute(text("DELETE FROM cluster WHERE name='TestCluster'"))
    conn.commit()
    conn.close()
    test_db.dispose()
