# tests/conftest.py
import pytest
import flask

import config

from app import app
from app.db import dbconnect
from app.models import Entry
from utils import date_before_today


@pytest.fixture
def client():
    app.config.from_object(config.TestConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def mock_db(mocker):
    mocker.patch("app.models.dbconnect")
    return True


@pytest.fixture
def db_conn():
    # assume the database has been freshly created
    with dbconnect() as conn:
        # seed with sample data to get started
        load_entries()

        yield conn

        # drop all the stuff and tables
        sqls = ["DELETE FROM entries;"]
        for sql in sqls:
            conn.execute(sql)


def load_entries() -> None:
    seeds = [
        {"text": "first entry", "date": date_before_today(1)},
        {"text": "it's another entry", "date": date_before_today(3)},
        {"text": "most recent one", "date": date_before_today(100)},
    ]
    for seed in seeds:
        Entry.create(content=seed["text"], date=seed["date"])
