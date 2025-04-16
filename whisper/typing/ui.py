"""
This module provides typing support for ui package.
"""

from typing import List, Literal, Callable, TypedDict

# General / Common
Empty = Literal[""]
ScreenUnit = float | str
Cursor = str | List[str]
Anchor = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
Relief = Literal["flat", "groove", "raised", "solid", "sunken"]
Compound = Literal["none", "bottom", "top", "left", "right", "center"]

# Label
LabelJustify = Literal["w", "center", "e"]

# Button
BUttonCmd = Callable[[], None] | Empty
ButtonState = Literal["normal", "active", "disabled"]

# Entry
EntryState = Literal["disabled", "normal", "readonly"]
EntryJustify = Literal["center", "left", "right"]
EntryValidateWhen = Literal["all", "focus", "focusin", "focusout", "key", "none"]
EntryValidateOpt = Literal["%d", "%i", "%P", "%s", "%v", "%S", "%V", "%W"]
EntryCmd = str | list[str] | tuple[str, ...] | Callable[[], bool]

# Font
class TkFontOpts(TypedDict):
    name: str
    family: str
    size: int
    weight: Literal["bold", "normal"]
    slant: Literal["italic", "roman"]
    underline: bool
    overstrike: bool

# tkinter palette
TkPaletteOpts = Literal[
    "activeBackground",
    "activeForeground",
    "background",
    "disabledBackground",
    "disabledForeground",
    "foreground",
    "highlightBackground",
    "highlightColor",
    "insertBackground",
    "selectBackground",
    "selectColor",
    "selectForeground",
    "troughColor"
]

class TkPalette(TypedDict):
    activeBackground: str
    activeForeground: str
    background: str
    disabledBackground: str
    disabledForeground: str
    foreground: str
    highlightBackground: str
    highlightColor: str
    insertBackground: str
    selectBackground: str
    selectColor: str
    selectForeground: str
    troughColor: str
