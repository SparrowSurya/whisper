"""
This module provides form labels.
"""

import tkinter as tk
from typing import Mapping

from whisper.ui import Container, Label
from whisper.typing import (
    Misc as _Misc,
    LabelColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
)


class Asterisk(Label):
    """Required indicator on form label."""

    def __init__(self, master: _Misc, *, text: str, **kwargs):
        Label.__init__(self, master, text=text, **kwargs)

    @classmethod
    def default_colorscheme(cls):
        return { **Label.default_colorscheme(), "foreground": "red" }


class FormLabel(Container):
    """Custom form label with support to required `*` indicator."""

    def __init__(self,
        master: tk.Misc,
        *,
        text: str,
        required: str,
        **kwargs,
    ):
        Container.__init__(self, master, **kwargs)
        self.text = Label(self, text=text)
        self.asterisk = Asterisk(self, text=required)

    def setup(self):
        self.text.pack(side="left")
        self.asterisk.pack(side="left")


class FormErrorLabel(Label):
    """Custom form error label."""

    def show_error(self, error: str):
        self.config(text=error)

    def clear_error(self):
        self.config(text="")

    @classmethod
    def default_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return { **Label.default_colorscheme(), "foreground": "red" }
