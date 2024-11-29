import logging

from .app import Application
from .logger import stream_handler, file_handler


logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler, file_handler])

app = Application()
app.mainloop()
