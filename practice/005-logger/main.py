from abc import ABC, abstractmethod
import json
from enum import Enum

class FormatterAbstract(ABC):
    pass
    @abstractmethod
    def format(self, message): pass

class JsonFormatter(FormatterAbstract):

    def format(self, message):
        json_data = {
            "msg": message
        }
        return json.dumps(json_data)
    
class StringFormatter(FormatterAbstract):
    def format(self, message):
        return f"str({message})"


class LogStrategy(ABC):

    def __init__(self, formatters: FormatterAbstract):
        self.formatters = formatters

    @abstractmethod
    def log(self, message): pass


class ConsoleLoggerStrategy(LogStrategy):

    def log(self, message):
        for format in self.formatters:
            formatted_message = format.format(message)
            print(f"CONSOLE LOGGING: {formatted_message}")

    
class FileLoggerStrategy(LogStrategy):

    def log(self, message):
        for format in self.formatters:
            formatted_message = format.format(message)
            print(f"FILE LOGGING: {formatted_message}")


class DBLoggerStrategy(LogStrategy):

    def log(self, message):
        for format in self.formatters:
            formatted_message = format.format(message)
            print(f"DB LOGGING: {formatted_message}")




class LoggerType(Enum):
    INFO = 1
    DEBUG = 2
    ERROR = 3


class LoggerAbstract(ABC):
    
    def __init__(self, nxt_logprocessor=None):
        self.nxt_logprocessor = nxt_logprocessor

    def log(self, log_type: LoggerType, message: str):
        if self.nxt_logprocessor != None:
            self.nxt_logprocessor.log(log_type, message)


class InfoLogger(LoggerAbstract):
    log_type = LoggerType.INFO
    
    def __init__(self, nxt_logprocessor=None, logging_strategies: list[LogStrategy]=[]):
        self.logging_strategies = logging_strategies

        super().__init__(nxt_logprocessor)

    def log(self, log_type: LoggerType, message: str):
        if self.log_type == log_type:
            for logging_strategy in self.logging_strategies:
                logging_strategy.log(message)
        else:
            super().log(log_type, message)


class DebugLogger(LoggerAbstract):
    log_type = LoggerType.DEBUG
    
    def __init__(self, nxt_logprocessor=None, logging_strategies: list[LogStrategy]=[]):
        self.logging_strategies = logging_strategies

        super().__init__(nxt_logprocessor)

    def log(self, log_type: LoggerType, message: str):
        if self.log_type == log_type:
            for logging_strategy in self.logging_strategies:
                logging_strategy.log(message)
        else:
            super().log(log_type, message)


class ErrorLogger(LoggerAbstract):
    log_type = LoggerType.ERROR
    
    def __init__(self, nxt_logprocessor=None, logging_strategies: list[LogStrategy]=[]):
        self.logging_strategies = logging_strategies

        super().__init__(nxt_logprocessor)

    def log(self, log_type: LoggerType, message: str):
        if self.log_type == log_type:
            for logging_strategy in self.logging_strategies:
                logging_strategy.log(message)
        else:
            super().log(log_type, message)

formatters = [JsonFormatter(), StringFormatter()]
logging_strategies = [FileLoggerStrategy(formatters), ConsoleLoggerStrategy(formatters)]#, DBLoggerStrategy(formatters)]
logger = InfoLogger(DebugLogger(ErrorLogger(logging_strategies=logging_strategies), logging_strategies), logging_strategies)


logger.log(LoggerType.ERROR, "This is an error message")
logger.log(LoggerType.DEBUG, "This is an debug message")
logger.log(LoggerType.INFO, "This is an info message")
