from plogger.log_levels import LogLevel
from plogger.sink import Sink
from datetime import datetime

class Logger:
    sinks = [[]] * len(LogLevel)

    def __init__(self):
        raise RuntimeError("Singleton class's object not allowed")

    @staticmethod
    def add_sink(sink: Sink, log_levels: list[LogLevel]):
        for level in log_levels:
            if Logger.sinks[level.value]:
                Logger.sinks[level.value].append(sink)
                # raise RuntimeError("Sink already defined for the log level", level.value)
            else:
                Logger.sinks[level.value] = [sink]
        
    @staticmethod
    def log(log_level: LogLevel, msg: str, namespace: str, sink: Sink = None):
        now = datetime.now()
        if sink != None:
            sink.write(now, log_level, namespace, msg)
        elif Logger.sinks[log_level.value] != None:
            for x in Logger.sinks[log_level.value]:
                x.write(now, log_level, namespace, msg)

    
    