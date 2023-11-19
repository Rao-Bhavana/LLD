from abc import ABC,abstractmethod
from plogger.log_levels import LogLevel
from datetime import datetime

class Sink(ABC):
    def __init__():
        pass
    
    @abstractmethod
    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        pass

    @abstractmethod
    def stop(self):
        pass