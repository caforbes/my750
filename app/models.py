from datetime import date, datetime
from typing import Annotated, NamedTuple, Optional
from psycopg import DatabaseError, IntegrityError
from psycopg.rows import namedtuple_row
from psycopg.sql import Literal, SQL
from pydantic import BaseModel, StringConstraints

from app import app
from app.constants import MAX_ENTRY_LEN
from app.db import dbconnect


# DB integration


class Entry:
    @classmethod
    def count(self) -> int:
        """
        Count the number of Entries in the db.
        """
        sql_count = "SELECT count(id) FROM entries;"
        with dbconnect() as conn:
            result = conn.execute(sql_count).fetchone()

        if result is None:
            app.logger.error("Database error: Entry count could not be accessed")
            return 0
        else:
            return result[0]

    @classmethod
    def create(cls, content: str, date: date = date.today()) -> int:
        """
        Create a new Entry in the database.
        Uses the current date by default, or you can provide a date in the past.
        """
        if date > date.today():
            raise ValueError(
                "Entry cannot be created in the future; "
                "date must be for today or an earlier date."
            )

        sqlbit = SQL(
            "INSERT INTO entries (content, for_day) VALUES ({content}, {date});"
        ).format(content=content, date=date)

        try:
            with dbconnect() as conn:
                res = conn.execute(sqlbit)

            app.logger.info(f"DB: Created {res.rowcount} new entries")
            return res.rowcount
        except IntegrityError:
            app.logger.warning(f"DB: Attempt to create entry for duplicate day")
            return 0

    @classmethod
    def get_today(cls) -> Optional[NamedTuple]:
        """
        Get the entry in the database for today's date or return None.
        """
        sqlbit = """SELECT id, content, for_day, created, updated,
                           wordcount(content) AS wdcount
                    FROM entries
                    WHERE for_day = current_date;"""

        with dbconnect().cursor(row_factory=namedtuple_row) as conn:
            result = conn.execute(sqlbit).fetchone()

        return result

    @classmethod
    def get(cls, id: int) -> Optional[NamedTuple]:
        """
        Get the entry matching the provided id in the database.
        """
        sqlbit = SQL(
            """SELECT id, content, for_day, created, updated,
                      wordcount(content) AS wdcount
               FROM entries
               WHERE id = {id};"""
        ).format(id=id)

        with dbconnect().cursor(row_factory=namedtuple_row) as conn:
            result = conn.execute(sqlbit).fetchone()

        return result

    @classmethod
    def list(cls, limit: int = 10) -> list[NamedTuple]:
        """
        Get a list of entries in the database up to the limit, the most recent first.
        """
        sqlbit = SQL(
            """SELECT  id, content, for_day, created, updated,
                       wordcount(content) AS wdcount
               FROM entries
               ORDER BY for_day DESC LIMIT {limit};"""
        ).format(limit=Literal(limit))

        with dbconnect().cursor(row_factory=namedtuple_row) as conn:
            result = conn.execute(sqlbit).fetchall()

        return result

    @classmethod
    def update(cls, id: int, content: str) -> int:
        """
        Update the text of the entry matching the provided id in the database.
        """
        sqlbit = SQL(
            """UPDATE entries SET content = {content}, updated = now()
                              WHERE id = {id};"""
        ).format(id=id, content=content)

        with dbconnect() as conn:
            res = conn.execute(sqlbit)

        app.logger.info(f"DB: Updated {res.rowcount} entries")
        return res.rowcount

    @classmethod
    def delete(cls, id: int) -> int:
        """
        Delete the entry matching the provided id in the database.
        """
        sqlbit = SQL("""DELETE FROM entries WHERE id = {id};""").format(id=id)

        with dbconnect() as conn:
            res = conn.execute(sqlbit)

        app.logger.info(f"DB: Deleted {res.rowcount} entries")
        return res.rowcount


# Data validation schema


class EntrySchema(BaseModel):
    id: int
    created: datetime
    updated: datetime
    for_day: date
    content: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, min_length=1, max_length=MAX_ENTRY_LEN
        ),
    ]
