from plogger.file_sink import *

class AsyncFileSink(BaseFileSink):
    def __init__(self,
                 path: str,
                 log_level: LogLevel,
                 rotationAfterSzInBytes: int = -1,
                 format: str = "%H:%M:%S.%f - {log_level} - {namespace} - {msg}",
                 mode = 'a',
                 buffering = 1,
                 **kwargs):
        super().__init__(path, log_level, rotationAfterSzInBytes, format, mode, buffering, **kwargs)
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._thread = threading.Thread(target=self.run_async_loop)
        self._thread.setDaemon(True)
        self._thread.start()

    
    def run_async_loop(self):
        self._loop.run_forever()

    def write(self, tp: datetime, log_level: LogLevel, namespace: str, msg: str):
        if self._loop.is_running:
            self._loop.call_soon_threadsafe(super().write, tp, log_level, namespace, msg)

    def stop(self):
        super().close_file()
        self._loop.stop()
        self._thread.join()

    def __del__(self):
        self.stop()
        