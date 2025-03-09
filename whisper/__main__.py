"""
Command line utility for running the app.
"""

import logging

from .app import App
from .logger import stream_handler


logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])

app = App()
app.mainloop()
