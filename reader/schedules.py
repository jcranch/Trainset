"""
Parses the National Rail CIF format
"""


from warnings import warn

from base import *
from codes import Schedule, Misc



def all_in(l):
    return lambda x: all(c in l for c in x)


def parse_days(s):
    return dict(zip(Misc.days,(c == "1" for c in s)))


def parse_activities(s):
    activities = [s[i:i+2].strip() for i in xrange(0,len(s),2)]
    activities = [x for x in activities if x != ""]
    for x in activities:
        if x not in Schedule.train_activity:
            warn("activity = %r"%(x,), UnrecognisedWarning)
    return activities


def parse_timing_load(pt,s):
    "Takes a power type and a timing load"
    if pt == "DMU":
        if s in Schedule.dmu_timing_load:
            return Schedule.dmu_timing_load[s]
        elif s in set(["D1","D2","D3","D4","D1T"]):
            return s
    elif pt == "EMU":
        if s == "AT":
            return "Accelerated Timing"
        elif s.isdigit():
            return "EMU, type "+s
    elif pt in set(["D","E","ED"]):
        if s.isdigit():
            n = int(s)
            if n < 1000 or (n < 10000 and pt == "ED"):
                return s + " tonnes"
    return None


def YN_to_bool(c):
    if c == "Y":
        return True
    elif c == "N":
        return False
    else:
        raise IncoherentData("Should be Y or N")


def parse_manual_3alpha(s):
    if len(s)==7 and s[3:] == "----":
        return s[:3]
    else:
        raise IncoherentData('Should be a 3-alpha code followed by "----"')


def linereader(expected_record_type):
    """
    Decorator for safely reading lines.
    """

    def method_maker(f):

        def method(self):
            if self.record_type == expected_record_type:
                f(self)
                self.nextline()
            else:
                warn("Record type mismatch: wanted %r; got %r"%(expected_record_type, self.record_type), WeirdBehaviour)

        return method

    return method_maker



class ScheduleMachine():
    """
    A class parsing schedules. Intended to be subclassed to specify
    the write methods (at the bottom), and begin() and end()
    """

    def __init__(self,manual=False):
        self.manual = manual

    def nextline(self):
        try:
            self.line = next(self.iterator)
            self.record_type = self.line[:2]
        except StopIteration:
            self.line = None
            self.record_type = "EOF"

    
    @linereader("HD")
    def read_HD(self):
        # Header
        d = self.header
        l = self.line

        data(d, "user_identity", l[7:13])
        data(d, "user_date", l[16:22], fn=date_yymmdd)
        data(d, "extracted_time", l[22:32], fn=datetime_ddmmyyhhmm)
        data(d, "reference", l[32:39])
        data(d, "previous_reference", l[39:46])
        d["full"] = (l[46] == 'F')
        data(d, "version", l[47])
        data(d, "extract_start", l[48:54], fn=date_ddmmyy)
        data(d, "extract_end", l[54:60], fn=date_ddmmyy)


    @linereader("BS")
    def read_BS(self):
        # Basic schedule
        d = self.schedule
        l = self.line

        data(d, "type", l[2], test=Schedule.transaction_types)
        data(d, "uid", l[3:9])
        data(d, "date_runs_from", l[9:15], fn=date_yymmdd)
        data(d, "date_runs_to", l[15:21], fn=date_yymmdd)
        data(d, "days_run", l[21:28], fn=parse_days, strip=False)
        data(d, "bank_holiday_running", l[28], test=Schedule.bhx)
        data(d, "train_status", l[29], test=Schedule.status)
        data(d, "category", l[30:32], test=Schedule.category)
        data(d, "train_identity", l[32:36])
        data(d, "headcode", l[36:40])
        data(d, "train_service_code", l[41:49])
        data(d, "portion_id", l[49])
        data(d, "power_type", l[50:53], test=Schedule.power_type)
        data(d, "timing_load", l[53:57], testfn = lambda x: parse_timing_load(d.get("power_type",None), x))
        data(d, "speed", l[57:60], fn=int)
        data(d, "operating_chars", l[60:66], testfn=all_in(Schedule.operating_chars))
        data(d, "train_class", l[66], test=Schedule.train_class)
        data(d, "sleepers", l[67], test=Schedule.sleepers)
        data(d, "reservations", l[68], test=Schedule.reservations)
        data(d, "catering", l[69:73], testfn=all_in(Schedule.catering))
        data(d, "service_branding", l[73:77], testfn=all_in(Schedule.service_branding))
        data(d, "stp_indicator", l[79], test=Schedule.stp_indicator)


    @linereader("BX")
    def read_BX(self):
        d = self.schedule
        l = self.line

        data(d, "uic_code", l[6:11])
        data(d, "atoc_code", l[11:13], Schedule.atoc_code)
        data(d, "applicable_timetable", l[13], fn=YN_to_bool)
        data(d, "rsid", l[14:22])
        data(d, "data_source", l[22])
            

    @linereader("TI")
    def read_TI(self):
        d = self.tiploc
        l = self.line

        d["type"] = "insert"
        if self.manual:
            data(d, "3alpha", l[2:9], fn=parse_manual_3alpha)
        else:
            data(d, "tiploc_code", l[2:9])
        data(d, "capitals", l[9:11])
        data(d, "nalco", l[11:17])
        data(d, "nlc_check", l[17])
        data(d, "tps_description", l[18:44])
        data(d, "po_mcp_code", l[49:53])
        data(d, "crs_code", l[53:56])
        data(d, "description", l[56:72])


    @linereader("TA")
    def read_TA(self):
        d = self.tiploc
        l = self.line
        d["type"] = "amend"
        if self.manual:
            data(d, "3alpha", l[2:9], fn=parse_manual_3alpha)
        else:
            data(d, "tiploc_code", l[2:9])
        data(d, "capitals", l[9:11])
        data(d, "nalco", l[11:17])
        data(d, "nlc_check", l[17])
        data(d, "tps_description", l[18:44])
        data(d, "po_mcp_code", l[49:53])
        data(d, "crs_code", l[53:56])
        data(d, "description", l[56:72])
        if self.manual:
            data(d, "new_3alpha", l[72:79], fn=parse_manual_3alpha)
        else:
            data(d, "new_tiploc_code", l[72:79])


    @linereader("TD")
    def read_TD(self):
        d = self.tiploc
        l = self.line
        d["type"] = "delete"
        if self.manual:
            data(d, "3alpha", l[2:9], fn=parse_manual_3alpha)
        else:
            data(d, "tiploc_code", l[2:9])


    @linereader("AA")
    def read_AA(self):
        d = self.association
        l = self.line

        data(d, "type", l[2], test=Schedule.transaction_types)
        data(d, "main_uid", l[3:9])
        data(d, "associated_uid", l[9:15])
        data(d, "start_date", l[15:21], fn=date_yymmdd)
        data(d, "end_date", l[21:27], fn=date_yymmdd)
        data(d, "days", l[27:34], fn=parse_days, strip=False)
        data(d, "category", l[34:36], test=Schedule.association_category)
        data(d, "date_ind", l[36], test=Schedule.association_date_ind)
        data(d, "association_location", l[37:44])
        data(d, "base_suffix", l[44], test=[" ","2"])
        data(d, "main_suffix", l[45], test=[" ","2"])
        data(d, "association_type", l[47], test=Schedule.association_type)
        data(d, "stp_indicator", l[79], test=Schedule.stp_indicator)


    @linereader("TN")
    def read_TN(self):
        d = self.schedule
        l = self.line
        if "notes" not in d:
            notes = {}
            d["notes"] = notes
        else:
            notes = d["notes"]

        note_type = l[2].strip()
        if note_type not in notes:
            notes[note_type] = ""
        notes[note_type] = (notes[note_type] + "\n" + l[3:80]).strip()


    @linereader("LO")
    def read_LO(self):
        a = self.location
        l = self.line

        a["type"] = "origin"
        data(a, "location", l[2:10])
        data(a, "scheduled_departure", l[10:15], fn=time_hhmmx)
        data(a, "public_departure", l[15:19], fn=time_hhmm)
        data(a, "platform", l[19:22])
        data(a, "line", l[22:25])
        data(a, "engineering_allowance", l[25:27], fn=timedelta_minh)
        data(a, "pathing_allowance", l[27:29], fn=timedelta_minh)
        data(a, "train_activity", l[29:41], fn=parse_activities, testfn=lambda x: "TB" in x)
        data(a, "performance_allowance", l[41:43], fn=timedelta_minh)
        

    @linereader("LI")
    def read_LI(self):
        a = self.location
        l = self.line

        a["type"] = "intermediate"
        
        data(a, "location", l[2:10])
        data(a, "scheduled_arrival", l[10:15], fn=time_hhmmx)
        data(a, "scheduled_departure", l[15:20], fn=time_hhmmx)
        data(a, "scheduled_pass", l[20:25], fn=time_hhmmx)
        data(a, "public_arrival", l[25:29], fn=time_hhmm)
        data(a, "public_departure", l[29:33], fn=time_hhmm)
        data(a, "platform", l[33:36])
        data(a, "line", l[36:39])
        data(a, "path", l[39:42])
        data(a, "train_activity", l[42:54])
        data(a, "engineering_allowance", l[54:56], fn=timedelta_minh)
        data(a, "pathing_allowance", l[56:58], fn=timedelta_minh)
        data(a, "performance_allowance", l[58:60], fn=timedelta_minh)
 

    @linereader("CR")
    def read_CR(self):
        d = self.location
        l = self.line

        d["type"] = "change"
        data(d, "location", l[2:10])
        data(d, "category", l[10:12], test=Schedule.category)
        data(d, "identity", l[12:16])
        data(d, "headcode", l[16:20])
        data(d, "service_code", l[21:29])
        data(d, "portion_id", l[29])
        data(d, "power_type", l[30:33], test=Schedule.power_type)
        data(d, "timing_load", l[33:37], testfn = lambda x: parse_timing_load(d.get("power_type",None), x))
        data(d, "speed", l[37:40], fn=int)
        data(d, "operating_chars", l[40:46], testfn=all_in(Schedule.operating_chars))
        data(d, "train_class", l[46], test=Schedule.train_class)
        data(d, "sleepers", l[47], test=Schedule.sleepers)
        data(d, "reservations", l[48], test=Schedule.reservations)
        data(d, "connection_indicator", l[49], test=Schedule.connection_indicator)
        data(d, "catering", l[50:54], testfn=all_in(Schedule.catering))
        data(d, "service_branding", l[54:58], test=Schedule.service_branding)
        data(d, "uic_code", l[62:67])
        data(d, "rsid", l[67:75])


    @linereader("LT")
    def read_LT(self):
        a = self.location
        l = self.line

        a["type"] = "terminating"

        data(a, "location", l[2:10])
        data(a, "scheduled_arrival", l[10:15], fn=time_hhmmx)
        data(a, "public_arrival", l[15:19], fn=time_hhmm)
        data(a, "platform", l[19:22])
        data(a, "path", l[22:25])
        data(a, "train_activities", l[25:37], fn=parse_activities, testfn=lambda x: 'TF' in x)


    @linereader("LN")
    def read_LN(self):
        d = self.location
        l = self.line
        if "notes" not in d:
            notes = {}
            d["notes"] = notes
        else:
            notes = d["notes"]

        note_type = l[2].strip()
        if note_type not in notes:
            notes[note_type] = ""
        notes[note_type] = (notes[note_type] + "\n" + l[3:80]).strip()


    @linereader("ZZ")
    def read_ZZ(self):
        # Trailer
        pass


    @linereader("EOF")
    def finish(self):
        self.end()


    def parse(self,filename):

        with open(filename,'r') as f:
            self.begin()

            self.iterator = iter(f)
            self.nextline()

            self.header = {}
            self.read_HD()
            self.write_header()

            while self.record_type == "TI":
                self.tiploc = {}
                self.read_TI()
                self.write_tiploc()

            while self.record_type == "TA":
                self.tiploc = {}
                self.read_TA()
                self.write_tiploc()

            while self.record_type == "TD":
                self.tiploc = {}
                self.read_TD()
                self.write_tiploc()

            while self.record_type == "AA":
                self.association = {}
                self.read_AA()
                self.write_association

            while self.record_type == "BS":
                self.schedule = {}
                self.locations = []
                self.read_BS()
                if self.record_type == "BX":
                    self.read_BX()
                while self.record_type == "TN":
                    self.read_TN()
                while self.record_type == "LO":
                    self.location = {}
                    self.read_LO()
                    while self.record_type == "LN":
                        self.read_LN()
                    self.locations.append(self.location)
                while self.record_type == "CR" or self.record_type == "LI":
                    if self.record_type == "CR":
                        self.location = {}
                        self.read_CR()
                        self.locations.append(self.location)
                    self.location = {}
                    self.read_LI()
                    while self.record_type == "LN":
                        self.read_LN()
                    self.locations.append(self.location)
                while self.record_type == "LT":
                    self.location = {}
                    self.read_LT()
                    while self.record_type == "LN":
                        self.read_LN()
                    self.locations.append(self.location)
                self.schedule["locations"] = self.locations
                self.write_schedule()

            self.read_ZZ()
            self.finish()


    def write_header(self):
        "Stores self.header in the appropriate way"
        pass


    def write_schedule(self):
        "Stores self.schedule in the appropriate way"
        pass


    def write_tiploc(self):
        "Stores self.tiploc in the appropriate way"
        pass


    def write_association(self):
        "Stores self.association in the appropriate way"
        pass


    def begin(self):
        "Prepare for parsing run"
        pass


    def end(self):
        "Tidy up after parsing run"
        pass

