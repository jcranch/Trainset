import re
from datetime import date, time


def read_alf(filename):
    return list(read_alf_generator(filename))

def date_dd_mm_yyyy(s):
    return date(int(s[6:10]), int(s[3:5]), int(s[0:2]))

def read_alf_generator(filename):
    r = re.compile(",|=")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    with open(filename, 'r') as f:
        for l in f:
            a = dict(p.split("=") for p in l.split(","))
            d = {}
            d["Mode"] = a["M"]
            d["Origin"] = a["O"]
            d["Destination"] = a["D"]
            d["Duration"] = int(a["T"])
            d["Start Time"] = time(int(a["S"][:2]), int(a["S"][2:]))
            d["End Time"] = time(int(a["E"][:2]), int(a["E"][2:]))
            d["Priority"] = int(a["P"])
            if "F" in a:
                d["Start Date"] = date_dd_mm_yyyy(a["F"])
            if "U" in a:
                d["End Date"] = date_dd_mm_yyyy(a["U"])
            if "R" in a:
                d["Days"] = dict(zip(days, (c=='1' for c in a["R"])))
            yield d

if __name__ == "__main__":
    print list(read_alf('../traindata/trains-043/TTISF043.ALF'))
