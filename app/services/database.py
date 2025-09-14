import sqlite3
from pathlib import Path

from resources.dml import INSERT_USER
from resources.queries import SELECT_USER_BY_USERID, SELECT_USER_BY_USERNAME
from resources.schema import USER_TABLE_SCHEMA, MEETING_TABLE_SCHEMA

PATH = Path("data/meetings.db")


def init_db():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(USER_TABLE_SCHEMA)
    cursor.execute(MEETING_TABLE_SCHEMA)
    connection.commit()
    connection.close()


def create_user(username: str, hashed_password: str) -> str | None:
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(INSERT_USER, (username, hashed_password))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()


def get_user_by_username(username: str):
    connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(SELECT_USER_BY_USERNAME, (username,))
    row = cursor.fetchone()

    connection.close()

    return dict(row) if row else None


def get_user_by_id(user_id: int):
    connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(SELECT_USER_BY_USERID, (user_id,))
    row = cursor.fetchone()

    connection.close()

    return dict(row) if row else None
