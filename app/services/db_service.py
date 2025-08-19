import sqlite3
from pathlib import Path

PATH = Path("data/meetings.db")


def init_db():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    ddl = open("resources/schema.sql", "r").read()
    cursor.executescript(ddl)
    connection.commit()
    connection.close()


def save_meeting(filename, transcript, summary, pdf_path):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    insert_stmt = open("resources/dml.sql", "r").read()

    try:
        cursor.execute(insert_stmt, (filename, transcript, summary, pdf_path))
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

    select_stmt = "SELECT * FROM meetings WHERE id = ?"

    try:
        cursor.execute(select_stmt, (meeting_id,))
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

    select_stmt = "SELECT id, filename, created_at FROM meetings"

    try:
        cursor.execute(select_stmt)
        meetings = cursor.fetchall()
        return [{"id": meeting[0], "filename": meeting[1], "created_at": meeting[2]} for meeting in meetings]
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()
