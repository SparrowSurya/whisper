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


LOG_DIR = pathlib.Path("logs")
os.makedirs(LOG_DIR, exist_ok=True)


DATA_DIR = "data"
USER_SETTING_FILE = str(pathlib.Path(DATA_DIR, "user_setting.json"))
os.makedirs(os.path.dirname(USER_SETTING_FILE), exist_ok=True)
