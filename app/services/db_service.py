import sqlite3
from pathlib import Path

from resources.dml import INSERT_MEETING, INSERT_USER
from resources.queries import SELECT_MEETING_BY_ID, SELECT_ALL_MEETING, SELECT_USER_BY_USERNAME, SELECT_USER_BY_USERID
from resources.schema import MEETING_TABLE_SCHEMA, USER_TABLE_SCHEMA

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


def save_meeting(filename, transcript, summary, pdf_path):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(INSERT_MEETING, (filename, transcript, summary, pdf_path))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()


def get_meeting_by_id(meeting_id: int):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(SELECT_MEETING_BY_ID, (meeting_id,))
        meeting = cursor.fetchone()
        return meeting
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()


def get_all_meetings():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(SELECT_ALL_MEETING)
        meetings = cursor.fetchall()
        return [{"id": meeting[0], "filename": meeting[1], "created_at": meeting[2]} for meeting in meetings]
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()
