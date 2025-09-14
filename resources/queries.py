# This file contains SQL queries for the meetings database.

# Select query for a specific meeting by ID
SELECT_MEETING_BY_ID = "SELECT * FROM meetings WHERE user_id = ? AND id = ?"

# Select query to retrieve all meetings
SELECT_ALL_MEETING = "SELECT id, filename, created_at FROM meetings WHERE user_id = ? ORDER BY created_at DESC"

SELECT_USER_BY_USERNAME = "SELECT * FROM users WHERE username = ?"

SELECT_USER_BY_USERID = "SELECT * FROM users WHERE id = ?"
