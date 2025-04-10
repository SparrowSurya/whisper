"""
This module provides the settings variables.
"""

import os
import pathlib
from enum import StrEnum, auto


APP_NAME = pathlib.Path(__file__).parent.parts[-1]


class Env(StrEnum):
    """Project environments."""

    PROD = auto()
    DEV  = auto()
    TEST = auto()


ENV = Env(os.environ.get("WHISPER_ENV", "dev"))

LOGGING_FORMAT_STYLE = "{"
LOGFILE = str(pathlib.Path("logs", f"{APP_NAME}.log"))

# make sure above file exists
os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
