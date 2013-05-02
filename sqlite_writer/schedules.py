from reader.schedules import *



class SqliteScheduleMachine(ScheduleMachine):

    def __init__(self,cursor,manual=False):
        ScheduleMachine.__init__(self, manual=manual)
        self.cursor = cursor
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    services (
      uid CHAR(6),
      date_runs_from TEXT,
      date_runs_to TEXT,
      weekday INTEGER,
      bank_holiday_running TEXT,
      status TEXT,
      category TEXT,
      toc TEXT,
      rsid TEXT
    ); """)
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    waypoints (
      type TEXT,
      location TEXT,
      arrival TEXT,
      departure TEXT,
      platform TEXT,
      line TEXT,
      passengers TEXT      
    ); """)
