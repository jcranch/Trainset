"""
see "TTIS Timetables Data Interface Definition" p16 and thereafter
"""

import itertools

from base import *



class StationMachine():

    def read_header(self, l):
        d = {}
        if l[30:40] != "FILE-SPEC=":
            raise ConversionFailure("No 'FILE-SPEC=' in header")
        d["version"] = l[40:48].strip()
        d["created"] = datetime_dd_mm_yy_hh_mm_ss(l[48:65])
        d["sequence"] = int(l[68:70])
        self.write_header(d)


    def read_station(self, p3a, records):
        tiplocs = []
        for l in records:
            d = {}
            d["name"] = l[5:35].strip()
            d["cate_type"] = l[35]
            d["tiploc_code"] = l[36:43].strip()
            if l[43:46] != p3a:
                d["3alpha_code"] = l[43:46]
            d["easting"] = int(l[52:57])
            d["estimated"] = l[57] == "E"
            d["northing"] = int(l[58:63])
            d["change_time"] = int(l[63:65].strip())
            tiplocs.append(d)

        self.write_station({"3alpha_code":p3a, "tiplocs":tiplocs})


    def read_alias(self,l):
        d = {}
        d["name"] = l[5:35].strip()
        d["alias"] = l[36:66].strip()
        self.write_alias(d)


    def read_group(self,l):
        d = {}
        d["name"] = l[5:35].strip()
        d["stations"] = l[36:].strip().split()
        self.write_group(d)


    def parse(self,filename):

        def relevant(l):
            return l[0] in ["A", "L", "V"]

        def principal_3alpha(l):
            return l[49:52]

        with open(filename,'r') as f:

            relevant_lines = itertools.ifilter(relevant, f)
            grouped_lines = itertools.groupby(relevant_lines, lambda w: w[0])

            for (rectype, lines) in grouped_lines:

                if rectype == "A":
                    self.read_header(next(lines))
                    stations = itertools.groupby(lines, principal_3alpha)
                    for (p3a, records) in stations:
                        self.read_station(p3a, records)

                elif rectype == "L":
                    for l in lines:
                        self.read_alias(l)

                elif rectype == "V":
                    for l in lines:
                        self.read_group(l)


    def write_header(self,d):
        pass

    def write_station(self,d):
        pass

    def write_alias(self,d):
        pass

    def write_group(self,d):
        pass
