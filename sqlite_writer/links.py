from reader.links import *
from codes import Misc


class SqliteLinkMachine(LinkMachine):

    def __init__(self,cursor,style=None):
        LinkMachine.__init__(self, style=style)
        self.cursor = cursor
        self.everyday = dict((k,True) for k in Misc.days)
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    links (
      mode TEXT,
      origin TEXT,
      destination TEXT,
      duration INTEGER,
      start_time TEXT,
      end_time TEXT,
      start_date TEXT,
      end_date TEXT,
      weekday INT); """)

    def write_link(self, d):
        for (day,runs) in d.get("days",self.everyday).iteritems():
            if runs:

                start_time = d.get("start_time",None)
                if start_time is not None:
                    start_time = start_time.isoformat()

                end_time = d.get("end_time",None)
                if end_time is not None:
                    end_time = end_time.isoformat()

                self.cursor.execute("""
  INSERT INTO links (mode, origin, destination, duration, start_time, end_time, start_date, end_date, weekday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (d["mode"], d["origin"], d["destination"], d["duration"].seconds, start_time, end_time, d.get("start_date",None), d.get("end_date",None), day))
