"""
This module manages the logging part of the app.
"""

import sys
import logging


default_fmt = logging.Formatter(
    fmt="{levelname:<8} {threadName:<15} {name:<21}: {message}",
    style="{",
)
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(default_fmt)
stream_handler.setLevel(logging.DEBUG)
