"""
Contains the app related settings.
"""

from whisper.ui.theme import Theme

# client and server
CHUNK_SIZE = 4096
ENCODING  = "utf-8"

# server
TIMEOUT = 10 # seconds

# client ui
DEFAULT_THEME = Theme.from_json("./whisper/data/default-theme.json")