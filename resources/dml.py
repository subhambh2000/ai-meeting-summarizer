# Meeting table insert query
INSERT_MEETING = """INSERT INTO meetings (filename, transript, summary, pdf_path)
                 VALUES (?, ?, ?, ?)"""
INSERT_USER = """INSERT INTO users (username, hashed_password)
                 VALUES (?, ?)"""