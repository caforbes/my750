from datetime import date, datetime
from typing import Annotated
from psycopg.rows import Row, namedtuple_row
from pydantic import BaseModel, StringConstraints

from app import app
from app.constants import MAX_ENTRY_LEN
from app.db import dbconnect


# DB integration


class Entry:
    @classmethod
    def count(self):
        """
        Count the number of Entries in the db.
        """
        sql_count = "SELECT count(id) FROM entries;"
        with dbconnect() as conn:
            result = conn.execute(sql_count).fetchone()
        return result[0]

    @classmethod
    def create(cls, content: str, date: date = date.today()) -> bool:
        """
        Create a new Entry in the db.
        Uses the current date by default, or you can provide a date in the past.
        """
        if date > date.today():
            raise ValueError(
                "Entry cannot be created in the future; "
                "date must be for today or an earlier date."
            )

        sqlbit = (
            "INSERT INTO entries (content, for_day) VALUES (%(content)s, %(date)s);"
        )
        data = dict(content=content, date=date)

        with dbconnect() as conn:
            conn.execute(sqlbit, data)
            app.logger.info("DB: Added new Entry")

        return True

    @classmethod
    def get_today(cls) -> Row | None:
        """
        Get the entry in the database for today's date or return None.
        """
        sqlbit = f"""SELECT (id, content, for_day, created, updated)
                     FROM entries
                     WHERE for_day = current_date;"""

        with dbconnect().cursor(row_factory=namedtuple_row) as conn:
            result = conn.execute(sqlbit).fetchone()

        return result

    # TODO: get via id
    # @classmethod
    # def get(cls, id: int) -> bool:
    #     sqlbit = f"INSERT INTO {cls.table} (content) VALUES (%(content)s);"
    #     data = dict(content=content)

    #     # with dbconnect() as conn:
    #     #     result = conn.execute(sqlbit, data)

    # TODO: list
    # TODO: update
    # TODO: delete

    # TODO: any custom functions like stats reading, etc


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
