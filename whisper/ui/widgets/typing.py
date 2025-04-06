"""
This modules provides various types used in the widget modules.
"""

from typing import Callable, Literal


__all__ = (
    "TkReliefOpts",
    "TkJustifyOpts",
    "TkPosOpts",
    "TkBtnCmd",
    "TkBtnStateOpts",
    "TkFontOpts",
    "TkPaletteOpts",
    "PaletteOpts",
)

TkReliefOpts = Literal["flat", "groove", "raised", "solid", "sunken"]
TkJustifyOpts = Literal["w", "center", "e"]
TkPosOpts = Literal["none", "bottom", "top", "left", "right", "center"]

TkBtnCmd = Callable[[], None]
TkBtnStateOpts = Literal["normal", "active", "disabled"]

TkFontOpts = Literal[
    "name",
    "family",
    "size",
    "weight",
    "slant",
    "underline",
    "overstrike",
]

TkPaletteOpts = Literal[
    "activeBackground",
    "activeForeground",
    "background",
    "disabledForeground",
    "foreground",
    "highlightBackground",
    "highlightColor",
    "insertBackground",
    "selectBackground",
    "selectColor",
    "selectForeground",
    "troughColor",
]

PaletteOpts = Literal[
    "surface0",
    "surface1",
    "surface2",
    "text",
    "subtext0",
    "subtext1",
    "overlay0",
    "overlay1",
    "overlay2",
    "base",
    "mantle",
    "crust",
    "white",
    "black",
    "red",
    "orange",
    "yellow",
    "green",
    "cyan",
    "blue",
    "violet",
    "magenta",
    "info",
    "success",
    "warning",
    "danger",
]
