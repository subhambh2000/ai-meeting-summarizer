import sqlite3

from fastapi.params import Depends

from app.auth.routes import get_current_user
from app.auth.schemas import UserOut
from app.services.database import PATH
from resources.dml import INSERT_MEETING
from resources.queries import SELECT_MEETING_BY_ID, SELECT_ALL_MEETING


def save_meeting(filename: str, transcript: str, summary: str, pdf_path, user_id: int):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(INSERT_MEETING, (user_id, filename, transcript, summary, pdf_path))
        connection.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()


def get_meeting_by_id(meeting_id: int, current_user: UserOut = Depends(get_current_user)):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(SELECT_MEETING_BY_ID, (current_user.id, meeting_id))
        meeting = cursor.fetchone()
        return meeting
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()


def get_all_meetings(current_user: UserOut = Depends(get_current_user)):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(SELECT_ALL_MEETING, (current_user.id,))
        meetings = cursor.fetchall()
        return [{"id": meeting[0], "filename": meeting[1], "created_at": meeting[2]} for meeting in meetings]
    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return None
    finally:
        connection.close()
