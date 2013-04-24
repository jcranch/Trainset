import re
from datetime import date, time

from codes import Misc


def read_alf(filename):
    return list(read_alf_generator(filename))

def date_dd_mm_yyyy(s):
    return date(int(s[6:10]), int(s[3:5]), int(s[0:2]))

def read_alf_generator(filename):
    r = re.compile(",|=")
    with open(filename, 'r') as f:
        for l in f:
            a = dict(p.split("=") for p in l.split(","))
            d = {}
            d["mode"] = a["M"]
            d["origin"] = a["O"]
            d["destination"] = a["D"]
            d["duration"] = int(a["T"])
            d["start time"] = time(int(a["S"][:2]), int(a["S"][2:]))
            d["end time"] = time(int(a["E"][:2]), int(a["E"][2:]))
            d["priority"] = int(a["P"])
            if "F" in a:
                d["start date"] = date_dd_mm_yyyy(a["F"])
            if "U" in a:
                d["end date"] = date_dd_mm_yyyy(a["U"])
            if "R" in a:
                d["days"] = dict(zip(Misc.days, (c=='1' for c in a["R"])))
            yield d
