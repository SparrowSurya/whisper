"""
This class provides custom foundation mixin class that can be used with tkinter widgets
to customize their appearance and behaviour.
"""

from .theme import ThemedTkWidgetMixin

from typing import Mapping


class CustomWidget(ThemedTkWidgetMixin):
    """Base mixin class for custom tkinter widgets."""

    def __init__(self):
        ThemedTkWidgetMixin.__init__(self)

    def setup(self):
        """Setup and configure widgets."""

    @classmethod
    def default_colorscheme(cls) -> Mapping[str, str]:
        return {}
