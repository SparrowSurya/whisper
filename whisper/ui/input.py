"""
This module provides custom input widget.
"""

import tkinter as tk
from enum import StrEnum
from typing import List

from .custom import CustomWidget
from whisper.typing import (
    Empty as _Empty,
    Relief as _Relief,
    ScreenUnit as _ScreenUnit,
    Cursor as _Cursor,
    EntryCmd as _EntryCmd,
    EntryState as _EntryState,
    EntryJustify as _EntryJustify,
    EntryValidateWhen as _EntryValidateWhen,
    EntryValidateOpt as _EntryValidateOpt,
)


# Source: https://www.tcl-lang.org/man/tcl8.5/TkCmd/entry.htm#M-validatecommand
class VcmdOpt(StrEnum):
    """Validation param options."""

    TYPE = "%d"
    """Type of action: 1 for insert, 0 for delete, or -1 for focus, forced or
    textvariable validation"""

    INDEX = "%i"
    """Index of char string to be inserted/deleted, if any, otherwise -1"""

    NEXT_VAL = "%P"
    """Value if the change is allowed."""

    PREV_VAL = "%s"
    """Value before the change."""

    CURR_VAL = "%v"
    """Current value."""

    VALUE = "%S"
    """The text string being inserted/deleted, if any, {} otherwise"""

    CAUSE = "%V"
    """The type of validation that triggered the callback (key, focusin, focusout,
    forced)"""

    WIDGET = "%W"
    """Name of widget."""


class Input(tk.Entry, CustomWidget):
    """Custom input widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        border: _ScreenUnit  = 0,
        borderwidth: _ScreenUnit = 0,
        cursor: _Cursor | _Empty = "",
        exportselection: bool = False,
        highlightthickness: _ScreenUnit = 0,
        insertborderwidth: _ScreenUnit = 0,
        insertofftime: int = 300,
        insertontime: int = 500,
        insertwidth: _ScreenUnit = 2,
        invalidcommand: _EntryCmd | _Empty = "",
        justify: _EntryJustify = "left",
        relief: _Relief = "sunken",
        selectborderwidth: _ScreenUnit = 0,
        state: _EntryState = "normal",
        takefocus: bool = True,
        validate_on: _EntryValidateWhen = "none",
        validate_params: List[_EntryValidateOpt] | _Empty = "",
        validatecommand: _EntryCmd | _Empty = "",
        variable: tk.Variable | _Empty = "",
        width: _ScreenUnit = 0,
        xscrollcommand: str = "",
    ):
        vcmd = ""
        if callable(validatecommand):
            vcmd, validatecommand = validatecommand, vcmd

        icmd = ""
        if callable(invalidcommand):
            icmd, invalidcommand = invalidcommand, icmd

        tk.Entry.__init__(self, master=master, border=border, borderwidth=borderwidth,
            cursor=cursor, exportselection=exportselection,
            highlightthickness=highlightthickness, insertborderwidth=insertborderwidth,
            insertofftime=insertofftime, insertontime=insertontime,
            insertwidth=insertwidth, invalidcommand=invalidcommand, justify=justify,
            relief=relief, selectborderwidth=selectborderwidth, state=state,
            takefocus=takefocus, validate=validate_on, validatecommand=validatecommand,
            textvariable=variable, width=width, xscrollcommand=xscrollcommand)

        if vcmd != "":
            vcmd = (self.register(vcmd), validate_params)

        if icmd != "":
            icmd = (self.register(icmd),)

        self.config(validatecommand=vcmd, invalidcommand=icmd)
        CustomWidget.__init__(self)

    def clear_value(self):
        """Clears value from input."""
        self.delete("0", "end")

    def set_value(self, value: str):
        """Set given value in input."""
        self.clear_value()
        self.insert("0", value)
