import sqlite3
from pathlib import Path

from resources.dml import INSERT_MEETING
from resources.queries import SELECT_MEETING_BY_ID, SELECT_ALL_MEETING
from resources.schema import MEETING_TABLE_SCHEMA

PATH = Path("data/meetings.db")


def init_db():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute(MEETING_TABLE_SCHEMA)
    connection.commit()
    connection.close()


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
