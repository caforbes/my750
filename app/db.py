import logging
import psycopg

from app import app


def dbconnect() -> psycopg.Connection:
    return psycopg.connect(app.config["PG_DATABASE_URI"])
