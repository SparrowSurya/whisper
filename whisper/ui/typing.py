"""
This modules provides various types used in ui  module.
"""

from typing import Union, Callable, Literal, TypedDict


__all__ = (
    "TkNone",
    "TkCursor",
    "TkScreenUnits",
    "TkAnchorOpts",
    "TkReliefOpts",
    "TkJustifyOpts",
    "TkPosOpts",
    "TkBtnCmd",
    "TkBtnStateOpts",
    "TkEntryStateOpts",
    "TkEntryJustifyOpts",
    "TkEntryValidateOpts",
    "TkEntryValidateCmd",
    "TkEntryInvalidateCmd",
    "TkFontOpts",
    "TkPaletteOpts",
    "PaletteOpts",
)


TkNone = Literal[""]
TkCursor = str
TkScreenUnits = Union[str, float]

TkAnchorOpts = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]

TkReliefOpts = Literal["flat", "groove", "raised", "solid", "sunken"]
TkJustifyOpts = Literal["w", "center", "e"]
TkPosOpts = Literal["none", "bottom", "top", "left", "right", "center"]

TkBtnCmd = Callable[[], None]
TkBtnStateOpts = Literal["normal", "active", "disabled"]

TkEntryStateOpts = Literal["disabled", "normal", "readonly"]
TkEntryJustifyOpts = Literal["center", "left", "right"]
TkEntryValidateOpts = Literal["all", "focus", "focusin", "focusout", "key", "none"]
TkEntryValidateCmd = Callable[[str, str, str, int], bool]
TkEntryInvalidateCmd = Callable[[], None]


class TkFontOpts(TypedDict):

    name: str
    family: str
    size: int
    weight: Literal["bold", "normal"]
    slant: Literal["italic", "roman"]
    underline: bool
    overstrike: bool


class TkPaletteOpts(TypedDict):

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


class PaletteOpts(TypedDict):

    surface0: str
    surface1: str
    surface2: str
    text: str
    subtext0: str
    subtext1: str
    overlay0: str
    overlay1: str
    overlay2: str
    base: str
    mantle: str
    crust: str
    white: str
    black: str
    red: str
    orange: str
    yellow: str
    green: str
    cyan: str
    blue: str
    violet: str
    magenta: str
    info: str
    success: str
    warning: str
    danger: str
