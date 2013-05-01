import re
from datetime import date, time

from base import *
from codes import Misc


def read_flf(filename):
    with open(filename,'r') as f:
        for l in f:
            l = l.split()
            if l[0] != "END":
                d = {}
                d["mode"] = l[2]
                d["origin"] = l[4]
                d["destination"] = l[6]
                d["duration"] = timedelta(minutes = int(l[8]))
                yield d

def read_alf(filename):
    r = re.compile(",|=")
    with open(filename, 'r') as f:
        for l in f:
            a = dict(p.split("=") for p in l.split(","))
            d = {}
            d["mode"] = a["M"]
            d["origin"] = a["O"]
            d["destination"] = a["D"]
            d["duration"] = timedelta(minutes = int(a["T"]))
            d["start_time"] = time(int(a["S"][:2]), int(a["S"][2:]))
            d["end_time"] = time(int(a["E"][:2]), int(a["E"][2:]))
            d["priority"] = int(a["P"])
            if "F" in a:
                d["start_date"] = date_dd_mm_yyyy(a["F"])
            if "U" in a:
                d["end_date"] = date_dd_mm_yyyy(a["U"])
            if "R" in a:
                d["days"] = dict(zip(Misc.days, (c=='1' for c in a["R"])))
            yield d


class LinkMachine():

    def __init__(self, style=None):
        if style=="fixed":
            self.style = "fixed"
            self.linkreader = read_flf
        elif style=="additional":
            self.style = "additional"
            self.linkreader = read_alf
        else:
            raise ConversionFailure("Argument 'style' must be 'fixed' or 'additional'")

    def parse(self,filename):
        for d in self.linkreader(filename):
            self.write_link(d)

    def write_link(self,d):
        pass
