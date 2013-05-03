from reader.schedules import *



class SqliteScheduleMachine(ScheduleMachine):

    everyday = dict((k,True) for k in Misc.days)

    def __init__(self, cursor, manual=False):
        ScheduleMachine.__init__(self, manual=manual)
        self.cursor = cursor
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    services (
      uid TEXT,
      date_runs_from TEXT,
      date_runs_to TEXT,
      weekday INTEGER,
      bank_holiday_running TEXT,
      status TEXT,
      category TEXT,
      toc TEXT,
      trainid TEXT,
      rsid TEXT
    ); """)
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    waypoints (
      uid TEXT,
      type TEXT,
      location TEXT,
      arrival_time TEXT,
      departure_time TEXT,
      platform TEXT,
      line TEXT,
      passengers TEXT
    ); """)


    def write_tiploc(self):
        pass # we could consider looking up self.tiploc to see that we've stored it already

    def write_schedule(self):
        "Stores self.schedule in the appropriate way"
        d = self.schedule
        uid = d.get("uid",None)
        date_runs_from = d.get("date_runs_from",None)
        date_runs_to = d.get("date_runs_to",None)
        bankhols = d.get("bank_holiday_running",None)
        status = d.get("train_status",None)
        category = d.get("category",None)
        toc = d.get("atoc_code",None)
        trainid = d.get("train_identity",None)
        rsid = d.get("rsid",None)

        for (day,runs) in d.get("days_run",self.everyday).iteritems():
            if runs:
                self.cursor.execute("""
  INSERT INTO services (uid, date_runs_from, date_runs_to, weekday, bank_holiday_running, status, category, toc, trainid, rsid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",(uid, date_runs_from, date_runs_to, day, bankhols, status, category, toc, trainid, rsid))

        for l in d["locations"]:
            ltype = l["type"]
            location = l["location"]
            if "public_arrival" in l:
                arrival_time = l["public_arrival"].isoformat()
            else:
                arrival_time = None
            if "public_departure" in l:
                departure_time = l["public_departure"].isoformat()
            else:
                departure_time = None
            line = l.get("line",None)
            platform = l.get("platform",None)
            a = l.get("train_activity",None)
            if a is not None and ("D" in a or "T" in a or "U" in a):
                passengers = "Y"
            else:
                passengers = None
            self.cursor.execute("""
  INSERT INTO waypoints (uid, type, location, arrival_time, departure_time, platform, line, passengers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",(uid, ltype, location, arrival_time, departure_time, platform, line, passengers))




