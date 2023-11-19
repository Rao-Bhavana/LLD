from plogger.log_levels import LogLevel
from plogger.sink import Sink
from datetime import datetime

class Logger:
    sinks = [None] * len(LogLevel)

    def __init__(self):
        raise RuntimeError("Singleton class's object not allowed")

    @staticmethod
    def add_sink(sink: Sink, log_levels: list[LogLevel]):
        for level in log_levels:
            Logger.sinks[level.value] = sink
        
    @staticmethod
    def log(log_level: LogLevel, msg: str, namespace: str, sink: Sink = None):
        now = datetime.now()
        if sink != None:
            sink.write(now, log_level, namespace, msg)
        elif Logger.sinks[log_level.value] != None:
            Logger.sinks[log_level.value].write(now, log_level, namespace, msg)