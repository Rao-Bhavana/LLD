from plogger.sink import Sink
from plogger.log_levels import LogLevel
from datetime import datetime
import gzip
import shutil
import os
import asyncio
import threading

class BaseFileSink(Sink):
    def __init__(self,
                 path: str,
                 log_level: LogLevel,
                 rotationAfterSzInBytes: int = -1,
                 format: str = "%H:%M:%S.%f - {log_level} - {namespace} - {msg}",
                 mode = 'a',
                 buffering = 1,
                 **kwargs):
        self._path = os.path.abspath(path)
        self._rotationAfterSzInBytes = rotationAfterSzInBytes
        self._cur_size = 0
        self._log_level = log_level
        self._format = format
        self._kwargs = {**kwargs, "mode": mode, "buffering": buffering}
        self._file = None

        # creation of log file
        self.open_file()
      

    def open_file(self):
        dirname = os.path.dirname(self._path)
        os.makedirs(dirname, exist_ok=True) # create if directory doesn't exist
        self._file = open(self._path, **self._kwargs)

    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        if log_level.value > self._log_level.value:
            return
        
        updated_msg = self.update_msg(tp, log_level, namespace, msg, self._format)

        # now = datetime.now()
        # diff = now - tp
        # updated_msg += " " + str(diff.microseconds) + " - " + now.strftime("%H:%M:%S.%f")

        if self._rotationAfterSzInBytes != -1 and len(updated_msg) + 1 + self._cur_size >= self._rotationAfterSzInBytes:
            self.rotate_logs(tp)

        self._file.write(updated_msg + "\n")
        self._cur_size += (len(updated_msg) + 1)

    def rotate_logs(self, tp: datetime):
        self.close_file()
        new_path = self._path + "." + datetime.now().strftime("%H%M%S_%f")
        os.rename(self._path, new_path)

        with open(new_path, 'rb') as f_in:
            with gzip.open(new_path + '.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(new_path)
        self.open_file()
        self._cur_size = 0

    def close_file(self):
        self._file.flush()
        self._file.close()

    def stop(self):
        self.close_file()


