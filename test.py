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



def files_of_extension(e):
    n = len(e) + 1
    for (d,_,l) in os.walk("../traindata"):
        for f in l:
            if f[-4:]=="."+e:
                yield os.path.join(d,f)



class UndesirableOutput(Warning):
    pass



class TestScheduleMachine(ScheduleMachine):
    
    def dictcheck(self,kind,d):
        "Checks to see if d has any empty values"
        for (k,v) in d.iteritems():
            if v is None or v == "":
                warn("Found %s with null or empty value for %r"%(kind,k), UndesirableOutput)

    def write_header(self):
        self.dictcheck("header", self.header)

    def write_schedule(self):
        self.dictcheck("schedule", self.schedule)

    def write_tiploc(self):
        self.dictcheck("tiploc", self.tiploc)

    def write_association(self):
        self.dictcheck("association", self.association)

def test_schedules():
    for f in files_of_extension("MCA"):
        print
        print "%s:"%(f,)
        TestScheduleMachine().parse(f)



def test_fixed_links():
    for f in files_of_extension("FLF"):
        print
        print "%s:"%(f,)
        read_flf(f)


def test_additional_links():
    for f in files_of_extension("ALF"):
        print
        print "%s:"%(f,)
        read_alf(f)




if __name__=="__main__":

    everything = set(["schedules", "links"])

    if len(sys.argv) > 1:
        to_do = set(sys.argv[1:])
    else:
        to_do = everything

    if "links" in to_do:
        to_do.discard("links")
        to_do.update(["fixed_links", "additional_links"])

    ws = [("once", ".*", UnsupportedWarning),
          ("once", ".*", UnrecognisedWarning),
          ("once", ".*", WeirdBehaviour)]

    with WarningFilter(ws):

        if "fixed_links" in to_do:
            test_fixed_links()
            
        if "additional_links" in to_do:
            test_additional_links()

        if "schedules" in to_do:
            test_schedules()
