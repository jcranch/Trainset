#!/usr/bin/env python
"""
Test suite.
"""

import os
import sys
from warnings import warn

from base import *
from read_schedules import *
from read_fixed_links import *
from read_additional_links import *
from read_stations import *



def files_of_extension(e):
    n = len(e) + 1
    for (d,_,l) in os.walk("../traindata"):
        for f in l:
            if f[-4:]=="."+e:
                yield os.path.join(d,f)



def got(s,x):
    t = x in s
    if t:
        s.discard(x)
    return t



def do_all(e,f):
    for x in files_of_extension(e):
        print
        print x + ":"
        f(x)



class UndesirableOutput(Warning):
    pass



def dictcheck(kind,d):
    "Checks to see if d has any empty values"
    for (k,v) in d.iteritems():
        if v is None or v == "":
            warn("Found %s with null or empty value for %r"%(kind,k), UndesirableOutput)

class TestScheduleMachine(ScheduleMachine):

    def write_header(self):
        dictcheck("header", self.header)

    def write_schedule(self):
        dictcheck("schedule", self.schedule)

    def write_tiploc(self):
        dictcheck("tiploc", self.tiploc)

    def write_association(self):
        dictcheck("association", self.association)

class TestStationMachine(StationMachine):

    def write_header(self, d):
        dictcheck("header", d)

    def write_station(self, d):
        if d["3alpha_code"] == "":
            warn("No 3-alpha code in station", UndesirableOutput)
        for t in d["tiplocs"]:
            dictcheck("tiploc", t)

    def write_alias(self, d):
        dictcheck("alias", d)

    def write_group(self, d):
        dictcheck("group", d)

class TestFixedLinkMachine(FixedLinkMachine):

    def write_link(self, d):
        dictcheck("fixed link", d)

class TestAdditionalLinkMachine(AdditionalLinkMachine):

    def write_link(self, d):
        dictcheck("additional link", d)


if __name__=="__main__":

    everything = set(["schedules", "links", "stations"])

    if len(sys.argv) > 1:
        to_do = set(sys.argv[1:])
    else:
        to_do = everything

    if got(to_do,"links"):
        to_do.update(["fixed_links", "additional_links"])

    if got(to_do, "schedules"):
        to_do.update(["full_schedules", "update_schedules", "manual_schedules"])

    ws = [("once", ".*", UnsupportedWarning),
          ("once", ".*", UnrecognisedWarning),
          ("once", ".*", WeirdBehaviour)]

    with WarningFilter(ws):

        if got(to_do,"fixed_links"):
            do_all("FLF", TestFixedLinkMachine().parse)
            
        if got(to_do,"additional_links"):
            do_all("ALF", TestAdditionalLinkMachine().parse)

        if got(to_do,"full_schedules"):
            do_all("MCA", TestScheduleMachine().parse)

        if got(to_do,"update_schedules"):
            do_all("CFA", TestScheduleMachine().parse)

        if got(to_do,"manual_schedules"):
            do_all("ZTR", TestScheduleMachine(manual=True).parse)

        if got(to_do,"stations"):
            do_all("MSN", TestStationMachine().parse)

    if len(to_do) > 0:
        print "Unused tasks: %s"%(", ".join(to_do),)
