from reader.interchanges import *


class SqliteInterchangeMachine(InterchangeMachine):

    def __init__(self,cursor):
        self.cursor = cursor
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    interchanges (
      station_3alpha TEXT,
      arriving_toc TEXT,
      departing_toc TEXT,
      change_time INTEGER
    ); """)

    def write_interchange(self,d):
        self.cursor.execute("""
  INSERT INTO interchanges (station_3alpha, arriving_toc, departing_toc, change_time) VALUES (?, ?, ?, ?)""", (d["station_code"], d["arriving_toc"], d["departing_toc"], d.get("change_time",None)))

