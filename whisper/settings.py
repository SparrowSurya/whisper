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
DEFAULT_ICON_PATH = "./whisper/assets/default_icon.png"

# window titlebar height (win32 platform)
MIN_WINDOW_WIDTH = 256
MIN_WINDOW_HEIGHT = 52
TITLEBAR_HEIGHT = 40

TITLE = "Whisper"