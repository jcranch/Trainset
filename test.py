"""
Test suite.
"""

import os
import sys
from warnings import warn

from read_schedules import *



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
    for (d,_,l) in os.walk("../traindata"):
        for f in l:
            if f[-4:]==".MCA":
                print
                print "%s:"%(f,)
                TestScheduleMachine().parse(os.path.join(d,f))



if __name__=="__main__":

    everything = ["schedules"]
    to_do = sys.argv[1:] or everything

    for task in to_do:
        if task == "schedules":
            test_schedules()
