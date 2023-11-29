from plogger.sink import Sink
from plogger.log_levels import LogLevel
from datetime import datetime
import sys

class ConsoleSink(Sink):

    def __init__(self,
                 log_level: LogLevel,
                 format: str = "%H:%M:%S.%f - {log_level} - {namespace} - {msg}",
                 **kwargs):
        self._log_level = log_level
        self._format = format

    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        if log_level.value > self._log_level.value:
            return
        
        updated_msg = self.update_msg(tp, log_level, namespace, msg, self._format)

        sys.stdout.write(updated_msg + "\n")

    def stop(self):
        pass