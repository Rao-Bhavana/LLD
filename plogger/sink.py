from abc import ABC,abstractmethod
from plogger.log_levels import LogLevel
from datetime import datetime

class Sink(ABC):
    def __init__():
        pass
    
    @abstractmethod
    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        pass

    def update_msg(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str, format: str):
        updated_msg = tp.strftime(format)
        updated_msg = updated_msg.replace("{log_level}", log_level.name)
        updated_msg = updated_msg.replace("{namespace}", namespace)
        updated_msg = updated_msg.replace("{msg}", msg)

        return updated_msg

    @abstractmethod
    def stop(self):
        pass