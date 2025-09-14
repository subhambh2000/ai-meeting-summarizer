MEETING_TABLE_SCHEMA = """CREATE TABLE IF NOT EXISTS meetings
                          (
                              id         INTEGER PRIMARY KEY AUTOINCREMENT,
                              user_id    INTEGER NOT NULL,
                              filename   TEXT    NOT NULL,
                              transcript TEXT,
                              summary    TEXT,
                              pdf_path   TEXT,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              FOREIGN KEY (user_id) REFERENCES users (id)
                          )"""
USER_TABLE_SCHEMA = """CREATE TABLE IF NOT EXISTS users
                       (
                           id              INTEGER PRIMARY KEY AUTOINCREMENT,
                           username        TEXT NOT NULL UNIQUE,
                           hashed_password TEXT NOT NULL,
                           created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )"""