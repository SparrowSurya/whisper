"""
This module provides threadsafe logger for the application.
"""

import sys
import logging
from typing import Dict


simple = "{levelname}: {message}"
column = "{levelname:<8} {threadName:<15} {module:<12}: {message}"
detail = "{levelname} {asctime} {threadName} {taskName} {module}: {message}"

simple_fmt = logging.Formatter(fmt=simple, style='{')
column_fmt = logging.Formatter(fmt=column, style='{')
detail_fmt = logging.Formatter(fmt=detail, style='{')

_handlers: Dict[str, logging.Handler] = {}


def setup_logging(level: int = logging.DEBUG, logfile: str | None = None):
    """setup root logger and respective handlers."""
    global _handlers
    root = logging.getLogger()
    root.setLevel(level)

    while root.handlers:
        handler = root.handlers[0]
        root.removeHandler(handler)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(column_fmt)
    stdout_handler.setLevel(level)
    root.addHandler(stdout_handler)
    _handlers["stdout"] = stdout_handler

    if logfile is not None:
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(detail_fmt)
        file_handler.setLevel(level)
        root.addHandler(file_handler)
        _handlers["file"] = file_handler


def cleanup_logging():
    """free captured resources and close handlers."""
    global _handlers

    stdout_handler = _handlers.pop("stdout", None)
    if stdout_handler:
        stdout_handler.close()

    file_handler = _handlers.pop("file", None)
    if file_handler:
        file_handler.close()

    assert len(_handlers.items()) == 0, f"unclosed handlers: {_handlers}"
