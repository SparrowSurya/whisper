"""
This module contains the root widget of the app (after MainWindow).
"""

from whisper.ui.widgets import Container


class Root(Container):
    """Root widget of the application."""

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = master.app
