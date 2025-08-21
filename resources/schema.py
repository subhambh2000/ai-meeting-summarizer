MEETING_TABLE_SCHEMA = """CREATE TABLE IF NOT EXISTS meetings
                          (
                              id         INTEGER PRIMARY KEY AUTOINCREMENT,
                              filename   TEXT NOT NULL,
                              transcript TEXT,
                              summary    TEXT,
                              pdf_path   TEXT,
                              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                          )"""
