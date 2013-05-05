from datetime import date, datetime, time, timedelta
from warnings import filterwarnings, resetwarnings, warn



class ConversionFailure(Exception):
    """
    Unexplained failure.
    """
    pass

class IncoherentData(Exception):
    """
    Bad data, where good data was expected.
    """
    pass



class TrainsetWarning(Warning):
    """
    Base class for warnings related to the CIF format.
    """
    pass

class UnrecognisedWarning(TrainsetWarning):
    """
    To be raised when encountering mysterious values in the data.
    """
    pass

class UnsupportedWarning(TrainsetWarning):
    """
    To be raised when encountering data of a known sort that we do not
    currently support.
    """
    pass

class WeirdBehaviour(TrainsetWarning):
    """
    To be raised when encountering apparently malformed data.
    """
    pass



class WarningFilter():

    def __init__(self, filters):
        self.filters = filters

    def __enter__(self):
        for f in self.filters:
            filterwarnings(*f)

    def __exit__(self,etype,evalue,etraceback):
        resetwarnings()
        return False



def y2k_coding(n):
    """
    The system used to enforce Year 2000 compliance. I guess they
    propose to worry about Year 2060 compliance when the time comes.
    """
    if n < 60:
        return 2000 + n
    else:
        return 1900 + n

def w44_coding(n):
    """
    Another system used elsewhere to deal with the Y2K bug. The idea,
    surely a masterstroke of genius, is to add 44 to all year numbers.
    """
    return (1956 + n)

def date_dd_mm_yyyy(s):
    return date(int(s[6:10]), int(s[3:5]), int(s[0:2]))

def date_ddmmyy(s):
    return date(y2k_coding(int(s[4:6])), int(s[2:4]), int(s[0:2]))

def date_yymmdd(s):
    if s == "999999":
        return None # a standard null format
    else:
        return date(y2k_coding(int(s[0:2])), int(s[2:4]), int(s[4:6]))

def date_yymmdd44(s):
    """
    As the above, but with the bizarre "add 44" year convention in force.
    """
    if s == "999999":
        return None
    else:
        return date(w44_coding(int(s[0:2])), int(s[2:4]), int(s[4:6]))

def datetime_ddmmyyhhmm(s):
    """
    This is the single worst time encoding I have ever worked with.
    """
    return datetime(y2k_coding(int(s[4:6])), int(s[2:4]), int(s[0:2]), int(s[6:8]), int(s[8:10]))

def datetime_dd_mm_yy_hh_mm_ss(s):
    return datetime(y2k_coding(int(s[6:8])), int(s[3:5]), int(s[0:2]), int(s[9:11]), int(s[12:14]), int(s[15:17]))

def time_hhmm(s):
    return time(int(s[0:2]), int(s[2:4]))

def time_hhmmx(s):
    if s[-1] == "H":
        return time(int(s[0:2]), int(s[2:4]), 30)
    else:
        return time(int(s[0:2]), int(s[2:4]), 0)

def timedelta_minh(s):
    if s[-1] == "H":
        return timedelta(minutes = int(s[:-1].strip() or 0), seconds = 30)
    else:
        return timedelta(minutes = int(s.strip()))



def data(dictionary, fieldname, source, test=None, fn=None, testfn=None, strip=True):
    """
    Automates several standard patterns in extracting data from
    fixed-length records.
    """
    if strip:
        source = source.strip()
    if source == "":
        return False
    if fn is not None:
        try:
            source = fn(source)
        except IncoherentData:
            warn("%s = %r"%(fieldname, source), UnrecognisedWarning)
            return False
        if source is None:
            return False
    if test is not None and source not in test:
        warn("%s = %r"%(fieldname, source), UnrecognisedWarning)
    if testfn is not None and not testfn(source):
        warn("%s = %r"%(fieldname, source), UnrecognisedWarning)
    dictionary[fieldname] = source
    return True
