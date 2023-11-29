from plogger.file_sink import *

class SyncFileSink(BaseFileSink):
    def __init__(self,
                 path: str,
                 log_level: LogLevel,
                 rotationAfterSzInBytes: int = -1,
                 format: str = "%H:%M:%S.%f - {log_level} - {namespace} - {msg}",
                 mode = 'a',
                 buffering = 1,
                 **kwargs):
        super().__init__(path, log_level, rotationAfterSzInBytes, format, mode, buffering, **kwargs)
        
        self.lock = threading.Lock()

    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        with self.lock:
            super().write(tp, log_level, namespace, msg)

    def rotate_logs(self, tp: datetime):
        with self.lock:
            super().rotate_logs(tp)

    def close_file(self):
        with self.lock:
            super().close_file()

    def stop(self):
        self.close_file()

    def __del__(self):
        self.stop()
        