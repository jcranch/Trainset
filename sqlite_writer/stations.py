from reader.stations import *



class SqliteStationMachine(StationMachine):

    def __init__(self,cursor):
        self.cursor = cursor
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    stations (
      tiploc_code TEXT PRIMARY KEY,
      name TEXT,
      principal_3alpha TEXT NOT NULL,
      subsidiary_3alpha TEXT,
      easting INTEGER,
      northing INTEGER,
      change_time INTEGER
    );""")
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    aliases (
      name TEXT REFERENCES stations,
      alias TEXT
    ); """)
        cursor.execute("""
  CREATE TABLE IF NOT EXISTS
    groups (
      name TEXT,
      station TEXT
    ); """)

    def write_header(self,d):
        pass

    def write_station(self,d):
        p3a = d["3alpha"]
        for t in d["tiplocs"]:
            self.cursor.execute("""
  INSERT INTO stations (tiploc_code, name, principal_3alpha, subsidiary_3alpha, easting, northing, change_time) VALUES (?, ?, ?, ?, ?, ?, ?);""", (t.get("tiploc_code",None), t.get("name",None), p3a, t.get("3alpha",p3a), t.get("easting",None), t.get("northing",None), t.get("change_time",None)))

    def write_alias(self,d):
        self.cursor.execute("""
  INSERT INTO aliases (name, alias) VALUES (?, ?);""", (d["name"], d["alias"]))

    def write_group(self,d):
        name = d["name"]
        for station in d["stations"]:
            self.cursor.execute("""
  INSERT INTO groups (name, station) VALUES (?, ?);""", (name, station))


