import sys

from whisper.core import App


app = App(sys.argv[1:])
app.run()
