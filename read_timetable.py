"""
Parses the National Rail CIF format
"""


from datetime import date, datetime
from warnings import warn, filterwarnings

from codes import Timetable


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
    return datetime(y2k_coding(int(s[4:6])), int(s[2:4]), int(s[0:2]), int(s[6:8]), int(s[8:10]))

def date_yymmdd(s):
    return date(y2k_coding(int(s[0:2])), int(s[2:4]), int(s[4:6]))



def parse_timetable(filename, behaviour_on_unsupported_data = "once", behaviour_on_unrecognised_data = "once"):
    """

    The two arguments "behaviour_on_X_data" take values suitable for
    warning filters: typically, here, "once", "error" or "ignore".
    """

    filterwarnings(behaviour_on_unsupported_data, ".*", UnsupportedWarning)
    filterwarnings(behaviour_on_unrecognised_data, ".*", UnrecognisedWarning)

    transaction_types = {"N": "new",
                         "D": "delete",
                         "R": "revise"}

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


    with open(filename,'r') as f:
        header = None

        for l in f:
            record_type = l[:2]

            if record_type == "HD":
                # Header
                d = {}
                d["user_identity"] = l[7:13]
                d["user_date"] = date_yymmdd(l[16:22])
                d["extracted_time"] = datetime_ddmmyyhhmm(l[22:32])
                d["current_reference"] = l[32:39].strip()
                d["previous_reference"] = l[39:46].strip()
                d["full"] = (l[46] == 'F')
                d["version"] = l[47]
                d["extract_start"] = date_ddmmyy(l[48:54])
                d["extract_end"] = date_ddmmyy(l[54:60])
                if header is not None:
                    warn("Two header fields: overwriting the first", WeirdBehaviour)
                header = d

            elif record_type == "BS":
                # basic schedule
                d = {}
                d["type"] = transaction_types[l[2]]
                d["uid"] = l[3:9]
                d["date_runs_from"] = date_yymmdd(l[9:15])
                if l[15:21] == "999999":
                    d["date_runs_to"] = None
                else:
                    d["date_runs_to"] = date_yymmdd(l[15:21])

                d["days_run"] = dict(zip(days,(c == "1" for c in l[21:28])))

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


            else:
                warn("record type %r"%(record_type,), UnsupportedWarning)
                # warn("record type %r"%(record_type,), UnrecognisedWarning)


if __name__=="__main__":
    parse_timetable("../traindata/trains-043/TTISF043.MCA")
