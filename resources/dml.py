# Meeting table insert query
INSERT_MEETING = """INSERT INTO meetings (filename, transript, summary, pdf_path)
                 VALUES (?, ?, ?, ?)"""