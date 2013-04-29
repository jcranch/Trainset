from warnings import filterwarnings, resetwarnings, warn



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
