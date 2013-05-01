from datetime import timedelta
from warnings import warn

from base import *


def read_interchanges(filename):
    with open(filename,'r') as f:
        for l in f:
            l = l.split(",")
            d = {}

            if len(l[0]) != 3 or not l[0].isalpha():
                warn("Station 3-alpha code is misshapen: %r"%(l[0],), UnrecognisedWarning)
            d["station_code"] = l[0]

            if len(l[1]) != 2 or not l[1].isalpha():
                warn("Arriving TOC is misshapen: %r"%(l[1],), UnrecognisedWarning)
            d["arriving_toc"] = l[1]

            if len(l[2]) != 2 or not l[2].isalpha():
                warn("Departing TOC is misshapen: %r"%(l[2],), UnrecognisedWarning)
            d["departing_toc"] = l[2]

            if not l[3].isdigit():
                raise IncoherentData("interchange time is not an integer: %r"%(l[3],))
            d["interchange_time"] = timedelta(minutes = int(l[3]))

            yield d


class InterchangeMachine():

    def parse(self, filename):
        for d in read_interchanges(filename):
            self.write_interchange(d)

    def write_interchange(self,d):
        pass
