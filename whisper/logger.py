import sys
import logging
from pathlib import Path


default_fmt = logging.Formatter("%(levelname)-8s %(threadName)-15s %(name)-21s: %(message)s")
log_file = str(Path("logs", "whisper.log"))

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(default_fmt)
stream_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(default_fmt)
file_handler.setLevel(logging.DEBUG)
