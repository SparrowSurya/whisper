import logging
import sys


logger = logging.getLogger("App")
logger.setLevel(logging.DEBUG)

simple_fmt = logging.Formatter("%(levelname)s: %(message)s")

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(simple_fmt)

logger.addHandler(stream_handler)
