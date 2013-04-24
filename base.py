from warnings import filterwarnings, resetwarnings



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

    def __exit__(self):
        resetwarnings()
        return False
