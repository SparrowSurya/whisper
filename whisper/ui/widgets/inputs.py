"""
This module provides custom input widget.
"""

import tkinter as tk

from .custom import CustomWidget
from .typing import (TkEntryInvalidateCmd, TkEntryJustifyOpts, TkEntryStateOpts,
    TkReliefOpts, TkScreenUnits, TkEntryValidateCmd, TkEntryValidateOpts, TkCursor,
    TkNone)


class Input(tk.Entry, CustomWidget):
    """Custom input widget."""

    def __init__(self,
        master: tk.Misc,
        *,
        border: TkScreenUnits  = 0,
        borderwidth: TkScreenUnits = 0,
        cursor: TkCursor = "",
        exportselection: bool = False,
        highlightthickness: TkScreenUnits = 0,
        insertborderwidth: TkScreenUnits = 0,
        insertofftime: int = 300,
        insertontime: int = 500,
        insertwidth: TkScreenUnits = 2,
        invalidcommand: TkEntryInvalidateCmd | TkNone = "",
        justify: TkEntryJustifyOpts = "left",
        relief: TkReliefOpts = "sunken",
        selectborderwidth: TkScreenUnits = 0,
        state: TkEntryStateOpts = "normal",
        takefocus: bool = True,
        validate_on: TkEntryValidateOpts = "none",
        validatecommand: TkEntryValidateCmd | TkNone = "",
        variable: tk.Variable | TkNone = "",
        width: TkScreenUnits = 0,
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
            vcmd = (self.register(vcmd), "%P", "%s", "%S", "%d")

        if icmd != "":
            icmd = (self.register(icmd),)

        self.config(validatecommand=vcmd, invalidcommand=icmd)
        CustomWidget.__init__(self)
