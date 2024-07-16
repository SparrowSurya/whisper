"""
Contains the app related settings.
"""

from whisper.ui.theme import Theme

CHUNK_SIZE = 4096
ENCODING  = "utf-8"


DEFAULT_THEME = Theme.from_json("./whisper/data/default-theme.json")