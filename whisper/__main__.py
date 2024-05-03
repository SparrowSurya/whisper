import sys

from .app import App


app = App(sys.argv[1:])
app.start()
