from plogger.sink import Sink
from plogger.log_levels import LogLevel
from datetime import datetime
import gzip
import shutil
import os
import asyncio
import threading

class FileSink(Sink):
    def __init__(self,
                 path: str,
                 log_level: LogLevel,
                 rotationAfterSzInBytes: int = -1,
                 format: str = "%H:%M:%S.%f - {log_level} - {namespace} - {msg}",
                 is_async: bool = False,
                 mode = 'a',
                 buffering = 1,
                 **kwargs):
        self._path = os.path.abspath(path)
        self._rotationAfterSzInBytes = rotationAfterSzInBytes
        self._cur_size = 0
        self._log_level = log_level
        self._format = format
        self._is_async = is_async
        self._kwargs = {**kwargs, "mode": mode, "buffering": buffering}

        # creation of log file
        self.open_file()

        if self._is_async:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._thread = threading.Thread(target=self.run_async_loop)
            self._thread.setDaemon(True)
            self._thread.start()

    def run_async_loop(self):
        self._loop.run_forever()

    def open_file(self):
        dirname = os.path.dirname(self._path)
        os.makedirs(dirname, exist_ok=True) # create if directory doesn't exist
        self._file = open(self._path, **self._kwargs)


    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        if self._is_async:
            if self._loop.is_running:
                self._loop.call_soon_threadsafe(self.write_impl, tp, log_level, namespace, msg)
        else:
            self.write_impl(tp, log_level, namespace, msg)

    def write_impl(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        if log_level.value > self._log_level.value:
            return
        
        updated_msg = tp.strftime(self._format)
        updated_msg = updated_msg.replace("{log_level}", log_level.name)
        updated_msg = updated_msg.replace("{namespace}", namespace)
        updated_msg = updated_msg.replace("{msg}", msg)

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
        if self._is_async:
            self._loop.stop()
            self._thread.join()

    def __del__(self):
        self.stop()
        


