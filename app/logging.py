import asyncio
from logging import StreamHandler

LOGQ = None

class QLogHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        if LOGQ:
            LOGQ.put_nowait(msg)
