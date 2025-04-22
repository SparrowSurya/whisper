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


class Font(TypedDict, total=False):
    name: str
    family: str
    size: int
    weight: Literal["bold", "normal"]
    slant: Literal["italic", "roman"]
    underline: bool
    overstrike: bool


class TkPalette(TypedDict, total=False):
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


PaletteOpts = Literal[
    "rosewater",
    "flamingo",
    "pink",
    "mauve",
    "red",
    "maroon",
    "peach",
    "yellow",
    "green",
    "teal",
    "sky",
    "sapphire",
    "blue",
    "lavender",
    "text",
    "subtext1",
    "subtext0",
    "overlay2",
    "overlay1",
    "overlay0",
    "surface2",
    "surface1",
    "surface0",
    "base",
    "mantle",
    "crust",
    "danger",
    "warn",
    "success",
    "info",
    "accent",
]
