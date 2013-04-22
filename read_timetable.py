"""
Parses the National Rail CIF format
"""


from datetime import date, datetime, time, timedelta
from warnings import warn, filterwarnings

from codes import Timetable, Misc



class CIF_Warning(Warning):
    """
    Base class for warnings related to the CIF format.
    """
    pass

class UnrecognisedWarning(CIF_Warning):
    pass

class UnsupportedWarning(CIF_Warning):
    pass

class WeirdBehaviour(CIF_Warning):
    pass



def y2k_coding(n):
    """
    The system used to enforce Year 2000 compliance. I guess they
    propose to worry about Year 2060 compliance when the time comes.
    """
    if n < 60:
        return 2000 + n
    else:
        return 1900 + n

def date_ddmmyy(s):
    return date(y2k_coding(int(s[4:6])), int(s[2:4]), int(s[0:2]))

def datetime_ddmmyyhhmm(s):
    """
    This is the single worst time encoding I have ever worked with.
    """
    return datetime(y2k_coding(int(s[4:6])), int(s[2:4]), int(s[0:2]), int(s[6:8]), int(s[8:10]))

def date_yymmdd(s):
    return date(y2k_coding(int(s[0:2])), int(s[2:4]), int(s[4:6]))

def time_hhmm(s):
    return time(int(s[0:2]), int(s[2:4]))

def time_hhmmx(s):
    if s.strip() == "":
        return None
    elif s[4] == "H":
        return time(int(s[0:2]), int(s[2:4]), 30)
    else:
        return time(int(s[0:2]), int(s[2:4]), 0)

def timedelta_minh(s):
    if s.strip() == "":
        return None
    elif s[1] == "H":
        return timedelta(minutes = int(s[0].strip() or 0), seconds = 30)
    else:
        return timedelta(minutes = int(s.strip()))


def parse_activities(s):
    activities = [s[i:i+2].strip() for i in xrange(0,len(s),2)]
    activities = [x for x in activities if x != ""]
    for x in activities:
        if x not in Timetable.train_activity:
            warn("activity = %r"%(x,), UnrecognisedWarning)
    return activities


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



class TimetableMachine():
    """
    A class parsing timetables. Intended to be subclassed to specify
    the write methods (at the bottom), and begin() and end()
    """


    def __init__(self):

        self.transaction_types = {"N": "new",
                                  "D": "delete",
                                  "R": "revise"}


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
        d = {}
        l = self.line

        d["user_identity"] = l[7:13]
        d["user_date"] = date_yymmdd(l[16:22])
        d["extracted_time"] = datetime_ddmmyyhhmm(l[22:32])
        d["reference"] = l[32:39].strip()
        d["previous_reference"] = l[39:46].strip()
        d["full"] = (l[46] == 'F')
        d["version"] = l[47]
        d["extract_start"] = date_ddmmyy(l[48:54])
        d["extract_end"] = date_ddmmyy(l[54:60])

        self.header = d


    @linereader("BS")
    def read_BS(self):
        # Basic schedule
        d = self.schedule
        l = self.line

        d["type"] = self.transaction_types[l[2]]
        d["uid"] = l[3:9]
        d["date_runs_from"] = date_yymmdd(l[9:15])
        if l[15:21] == "999999":
            d["date_runs_to"] = None
        else:
            d["date_runs_to"] = date_yymmdd(l[15:21])

        d["days_run"] = dict(zip(Misc.days,(c == "1" for c in l[21:28])))

        bhx = l[28].strip()
        if bhx:
            d["bank_holiday_running"] = bhx
            if bhx not in Timetable.bhx:
                warn("bank holiday running code = %r"%(bhx,),UnrecognisedWarning)

        status = l[29].strip()
        if status:
            d["train_status"] = status
            if status not in Timetable.status:
                warn("status = %r"%(status,),UnrecognisedWarning)

        category = l[30:32].strip()
        if category:
            d["category"] = category
            if category not in Timetable.category:
                warn("category = %r"%(category,),UnrecognisedWarning)

        d["train_identity"] = l[32:36].strip()
        d["headcode"] = l[36:40]
        d["train_service_code"] = l[41:49]
        d["portion_id"] = l[49]

        power_type = l[50:53].strip()
        if power_type:
            d["power_type"] = power_type
            if power_type not in Timetable.power_type:
                warn("power_type = %r"%(power_type,),UnrecognisedWarning)
        d["timing_load"] = l[53:57].strip() # should validate this

        d["speed"] = int(l[57:60].strip() or 0)

        operating_chars = list(l[60:66].strip())
        d["operating_chars"] = operating_chars
        for c in operating_chars:
            if c not in Timetable.operating_chars:
                warn("operating_chars has %r"%(c,),UnrecognisedWarning)

        train_class = l[66].strip() or "B"
        d["train_class"] = train_class
        if train_class not in Timetable.train_class:
            warn("train_class = %r"%(train_class,),UnrecognisedWarning)  
        sleepers = l[67].strip()
        if sleepers:
            d["sleepers"] = sleepers
            if sleepers not in Timetable.sleepers:
                warn("sleepers = %r"%(sleepers,),UnrecognisedWarning)

        reservations = l[68].strip()
        if reservations:
            d["reservations"] = reservations
            if reservations not in Timetable.reservations:
                warn("reservations = %r"%(sleepers,),UnrecognisedWarning)

        catering = list(l[69:73].strip())
        d["catering"] = catering
        for c in catering:
            if c not in Timetable.catering:
                warn("catering has %r"%(c,),UnrecognisedWarning)

        service_branding = list(l[73:77].strip())
        d["service_branding"] = service_branding
        for c in service_branding:
            if c not in Timetable.service_branding:
                warn("service_branding has %r"%(c,),UnrecognisedWarning)


    @linereader("BX")
    def read_BX(self):
        d = self.schedule
        l = self.line
        
        uic_code = l[6:11].strip()
        if uic_code:
            d["uic_code"] = uic_code

        atoc_code = l[11:13].strip()
        if atoc_code:
            d["atoc_code"] = atoc_code
            if atoc_code not in Timetable.atoc_code:
                warn("atoc_code = %r"%(atoc_code,), UnrecognisedWarning)

        atc = l[13].strip()
        if atc == "Y":
            d["applicable_timetable"] = True
        elif atc == "N":
            d["applicable_timetable"] = False
        else:
            warn("atc = %r"%(atc,), UnrecognisedWarning)
            d["applicable_timetable"] = atc

        rsid = l[14:22].strip()
        if rsid:
            d["rsid"] = rsid

        data_source = l[22].strip()
        if data_source:
            d["data_source"] = data_source
            

    @linereader("TI")
    def read_TI(self):
        warn("Can't do TI yet",UnsupportedWarning)


    @linereader("TA")
    def read_TA(self):
        warn("Can't do TA yet",UnsupportedWarning)


    @linereader("TD")
    def read_TD(self):
        warn("Can't do TD yet",UnsupportedWarning)


    @linereader("AA")
    def read_AA(self):
        warn("Can't do AA yet",UnsupportedWarning)


    @linereader("CR")
    def read_CR(self):
        warn("Can't do CR yet",UnsupportedWarning)


    @linereader("TN")
    def read_TN(self):
        warn("Records of type TN are as yet undefined",UnsupportedWarning)


    @linereader("LO")
    def read_LO(self):
        a = self.location
        l = self.line

        a["type"] = "origin"
        a["location"] = l[2:10].strip()
        
        scheduled_departure = time_hhmmx(l[10:15])
        if scheduled_departure is not None:
            a["scheduled_departure"] = scheduled_departure

        a["public_departure"] = time_hhmm(l[15:19])
        a["platform"] = l[19:22].strip()
        a["line"] = l[22:25].strip()

        engineering_allowance = timedelta_minh(l[25:27])
        if engineering_allowance is not None:
            a["engineering_allowance"] = engineering_allowance

        pathing_allowance = timedelta_minh(l[27:29])
        if pathing_allowance is not None:
            a["pathing_allowance"] = pathing_allowance

        activities = parse_activities(l[29:41])
        if "TB" not in activities:
            warn("TB is not in train activities", WeirdBehaviour)
        a["train_activity"] = activities

        performance_allowance = timedelta_minh(l[41:43])
        if performance_allowance is not None:
            a["performance_allowance"] = performance_allowance
        

    @linereader("LI")
    def read_LI(self):
        a = self.location
        l = self.line

        a["type"] = "intermediate"
        a["location"] = l[2:10].strip()
        a["scheduled_arrival"] = time_hhmmx(l[10:15])
        a["scheduled_departure"] = time_hhmmx(l[15:20])
        a["scheduled_pass"] = time_hhmmx(l[20:25])
        a["public_arrival"] = time_hhmm(l[25:29])
        a["public_departure"] = time_hhmm(l[29:33])
        a["platform"] = l[33:36].strip()
        a["line"] = l[36:39].strip()
        a["path"] = l[39:42].strip()
        a["train_activity"] = parse_activities(l[42:54])
        
        engineering_allowance = timedelta_minh(l[54:56])
        if engineering_allowance is not None:
            a["engineering_allowance"] = engineering_allowance

        pathing_allowance = timedelta_minh(l[56:58])
        if pathing_allowance is not None:
            a["pathing_allowance"] = pathing_allowance

        performance_allowance = timedelta_minh(l[58:60])
        if performance_allowance is not None:
            a["performance_allowance"] = performance_allowance
 

    @linereader("LT")
    def read_LT(self):
        warn("Can't do LT yet",UnsupportedWarning)


    @linereader("LN")
    def read_LN(self):
        warn("Records of type LN are as yet undefined",UnsupportedWarning)


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
            self.header = None

            self.read_HD()
            self.write_header()

            while self.record_type == "TI":
                self.read_TI()

            while self.record_type == "TA":
                self.read_TA()

            while self.record_type == "TD":
                self.read_TD()

            while self.record_type == "AA":
                self.read_AA()

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
                    self.location = {}
                    if self.record_type == "CR":
                        self.read_CR()
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


    def begin(self):
        "Prepare for parsing run"
        pass


    def end(self):
        "Tidy up after parsing run"
        pass



def parse_timetable(filename, behaviour_on_unsupported_data = "once", behaviour_on_unrecognised_data = "once", behaviour_on_weird_behaviour = "error"):
    """
    The two arguments "behaviour_on_X_data" take values suitable for
    warning filters: typically, here, "once", "error" or "ignore".
    """

    filterwarnings(behaviour_on_unsupported_data, ".*", UnsupportedWarning)
    filterwarnings(behaviour_on_unrecognised_data, ".*", UnrecognisedWarning)
    filterwarnings(behaviour_on_weird_behaviour, ".*", WeirdBehaviour)

    TimetableMachine().parse(filename)



if __name__=="__main__":
    parse_timetable("../traindata/trains-043/TTISF043.MCA")
