"""
This module provides objects for storing themes and color palettes. It provides a mixin
class which can use the theme data and with its preferred palette attributes to
themeify tkinter widget.


classes
-------
* Palette - stores color information
* Theme - stores overall theme data
* ThemedTkWidgetMixin - mixin class to transform tkinter widget to preferred theme.
"""

from dataclasses import dataclass
from typing import Dict

from whisper.typing import (
    Font as _Font,
)


__all__ = (
    "Palette",
    "Theme",
    "ThemedTkWidgetMixin",
)


@dataclass(frozen=True)
class Palette:
    """Color palette for widget color attributes. Make sure that color values are
    provided as hexadecimal values or recogonised color names."""

    base: str
    mantle: str
    crust: str

    surface0: str
    surface1: str
    surface2: str

    text: str
    subtext0: str
    subtext1: str

    overlay0: str
    overlay1: str
    overlay2: str

    rosewater: str
    flamingo: str
    pink: str
    mauve: str
    red: str
    maroon: str
    peach: str
    yellow: str
    green: str
    teal: str
    sky: str
    sapphire: str
    blue: str
    lavender: str


@dataclass(frozen=True, repr=False)
class Theme:
    """A Theme data object."""

    name: str
    palette: Palette
    font: _Font


class ThemedTkWidgetMixin:
    """Tkinter based mixin class to provide theme to tkinter widget.

    Attributes:
    * colorscheme

    Methods:
    * get_colorscheme
    * set_theme
    * configure (taken from tkinter widget)
    """

    colorscheme: Dict[str, str] = {}
    """Mapping from tkinter attribute to palette attributes."""

    def get_colorscheme(self) -> Dict[str, str]:
        """Provides the colorscheme information."""
        return self.colorscheme

    def set_theme_self(self, theme: Theme):
        """Sets the theme on the widget."""
        scheme = self.get_colorscheme()
        data = {attr: theme.scheme[value] for attr, value in scheme.items()}
        self.configure(**data)

    def set_theme_child(self, theme: Theme):
        """Sets theme on child widgets."""
        for child in self.winfo_children():
            child.set_theme(theme)

    def set_theme(self, theme: Theme):
        """Sets theme on itself and children."""
        self.set_theme_self(theme)
        self.set_theme_child(theme)

    def configure(self, *args, **kwargs):
        """This must be provided by the tkinter widget."""
        cls = type(self).__name__
        raise RuntimeError(f"{cls} class must be used with tkinter widget.")

    def winfo_children(self):
        """This must be provided by the tkinter widget."""
        cls = type(self).__name__
        raise RuntimeError(f"{cls} class must be used with tkinter widget.")
