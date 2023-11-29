from plogger.logger import Logger
from plogger.file_sink import BaseFileSink
from plogger.async_file_sink import AsyncFileSink
from plogger.sync_file_sink import SyncFileSink
from plogger.console_sink import ConsoleSink
from plogger.log_levels import LogLevel
import time

if __name__ == "__main__":
    Logger.add_sink(BaseFileSink('log/normal.log', LogLevel.WARN, 1000, format="%H:%M:%S.%f | {log_level} | {namespace} | {msg}"), 
                    log_levels = [LogLevel.WARN, LogLevel.ERROR])
    Logger.add_sink(AsyncFileSink('log/async.log', LogLevel.WARN, 1000, format="%H:%M:%S.%f | {log_level} | {namespace} | {msg}"), 
                    log_levels = [LogLevel.WARN, LogLevel.ERROR, LogLevel.FATAL])
    Logger.add_sink(SyncFileSink('log/sync.log', LogLevel.WARN, 1000, format="%H:%M:%S.%f | {log_level} | {namespace} | {msg}"), 
                    log_levels = [LogLevel.FATAL])
    Logger.add_sink(ConsoleSink(LogLevel.DEBUG),
                    log_levels = [LogLevel.DEBUG, LogLevel.INFO])

    Logger.log(LogLevel.INFO, "This is info log -- should be on console", "main")
    Logger.log(LogLevel.ERROR, "error log", "main")
    Logger.log(LogLevel.FATAL, "Fatal log", "main")

    # Test rotation
    # for i in range(100):
    #     Logger.log(LogLevel.ERROR, "$", "main")

    # Test async
    # random_sink1 = FileSink('log/random1.log', LogLevel.DEBUG, is_async=True)
    # random_sink2 = FileSink('log/random2.log', LogLevel.DEBUG, is_async=False)
    
    # count = 10000
    # t1 = time.time_ns()

    # for i in range(count):
    #     Logger.log(LogLevel.DEBUG, "Random debug log", "Random1", sink=random_sink1)

    # t2 = time.time_ns()

    # for i in range(count):
    #     Logger.log(LogLevel.DEBUG, "Random debug log", "Random2", sink=random_sink2)

    # t3 = time.time_ns()

    # print(f"Async: {(t2-t1)/count} ns")
    # print(f"Sync: {(t3-t2)/count} ns")


