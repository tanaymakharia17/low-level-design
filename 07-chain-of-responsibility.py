"""

E.g.:
ATM/Vending machines -> someone add 2515 to withdraw. First level is max 2000 rs notesthen max 500 rs notes then 
max 10 notes and then max 5 notes. If present withdraw this amount else give not available 
Logger: below
"""

from abc import ABC
from enum import Enum


class LogEnum(Enum):
    INFO = 1
    DEBUG = 2
    ERROR = 3

class LogProcessor(ABC):
    nxt_logprocessor = None
    def __init__(self, nxt_logprocessor):
        self.nxt_logprocessor = nxt_logprocessor

    def log(self, log_level, message):
        if self.nxt_logprocessor != None:
            self.nxt_logprocessor.log(log_level, message)


class InfoLogProcessor(LogProcessor):
    log_type = LogEnum.INFO

    def __init__(self, nxt_logprocessor):
        super().__init__(nxt_logprocessor)
    
    def log(self, log_level, message):
        if log_level == self.log_type:
            print("INFO:", message)
        else:
            super().log(log_level, message)

class DebugLogProcessor(LogProcessor):
    log_type = LogEnum.DEBUG

    def __init__(self, nxt_logprocessor):
        super().__init__(nxt_logprocessor)
    
    def log(self, log_level, message):
        if log_level == self.log_type:
            print("DEBUG:", message)
        else:
            super().log(log_level, message)

class ErrorLogProcessor(LogProcessor):
    log_type = LogEnum.ERROR

    def __init__(self, nxt_logprocessor):
        super().__init__(nxt_logprocessor)
    
    def log(self, log_level, message):
        if log_level == self.log_type:
            print("ERROR:", message)
        else:
            super().log(log_level, message)







logger = InfoLogProcessor(DebugLogProcessor(ErrorLogProcessor(None)))
logger.log(LogEnum.ERROR, "This is an error")
logger.log(LogEnum.DEBUG, "This is a debug")
logger.log(LogEnum.INFO, "This is an info")
