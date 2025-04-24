"""
This class provides custom foundation mixin class that can be used with tkinter widgets
to customize their appearance and behaviour.
"""

from .theme import ThemedTkWidgetMixin


class CustomWidget(ThemedTkWidgetMixin):
    """Base mixin class for custom tkinter widgets."""

    def __init__(self):
        ThemedTkWidgetMixin.__init__(self)

    def setup(self):
        """Setup and configure widgets."""
