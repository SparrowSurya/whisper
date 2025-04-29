"""
This module provides threadsafe logger for the application.
"""

import sys
import logging
from typing import List


simple = "{levelname}: {message}"
column = "{levelname:<8} {threadName:<15} {module:<12}: {message}"
detail = "{levelname} {asctime} {threadName} {taskName} {module}: {message}"

simple_fmt = logging.Formatter(fmt=simple, style='{')
column_fmt = logging.Formatter(fmt=column, style='{')
detail_fmt = logging.Formatter(fmt=detail, style='{')


def stdout_handler() -> logging.Handler:
    """Provides stdout handler for terminal."""
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(column_fmt)
    handler.setLevel(logging.DEBUG)
    return handler


def file_handler(filepath: str) -> logging.Handler:
    """Provides file handler for storage."""
    handler = logging.FileHandler(filepath)
    handler.setFormatter(detail_fmt)
    handler.setLevel(logging.DEBUG)
    return handler


class Logger(logging.Logger):
    """Custom application logger,"""

    def __init__(self, name: str, level: int, handlers: List[logging.Handler]):
        super().__init__(name, level)
        for handler in handlers:
            self.addHandler(handler)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func = None,
        extra = None, sinfo = None,
    ):
        # python version >= 3.12 does not support overriding key in LogRecord
        # python version <= 3.11 does require all keys and don't handles missing one
        if sys.version_info.minor <= 11:
            if extra is None:
                extra = {}
            if "taskName" not in extra:
                extra["taskName"] = "None"

        return super().makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
