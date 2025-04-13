"""
This module provides threadsafe logger for the application.
"""

import sys
import logging
from typing import Sequence

from whisper.settings import LOGFILE, LOGGING_FORMAT_STYLE


simple = "{levelname}: {message}"
column = "{levelname:<8} {threadName:<15} {module:<12}: {message}"
detail = "{levelname} {asctime} {threadName} {taskName} {module}: {message}"

simple_fmt = logging.Formatter(fmt=simple, style=LOGGING_FORMAT_STYLE)
column_fmt = logging.Formatter(fmt=column, style=LOGGING_FORMAT_STYLE)
detail_fmt = logging.Formatter(fmt=detail, style=LOGGING_FORMAT_STYLE)



stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(column_fmt)
stdout_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOGFILE)
file_handler.setFormatter(detail_fmt)
file_handler.setLevel(logging.DEBUG)


class Logger(logging.Logger):
    """Custom application logger,"""

    def __init__(self, name: str, level: int, handlers: Sequence[logging.Handler]):
        super().__init__(name, level)
        for handler in handlers:
            self.addHandler(handler)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func = None,
        extra = None, sinfo = None,
    ):
        if extra is None:
            extra = {}
        if "taskName" not in extra:
            extra["taskName"] = "N/A"
        return super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
