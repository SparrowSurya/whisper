"""
This module provides form labels.
"""

import tkinter as tk
from typing import Mapping, Any

from whisper.ui import Container, Label
from whisper.typing import (
    LabelColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
)

DEFAULT_INDICATOR = " *"

class Asterisk(Label):
    """Required indicator on label."""

    indicator = DEFAULT_INDICATOR
    """Marker shown by label."""

    indicator_colorscheme: Mapping[_ColorAttr, _PaletteOpts] = { "foreground": "red" }
    """Colorscheme overrides."""

    def __init__(self, master: tk.Misc, *, text: str = DEFAULT_INDICATOR, **kwargs):
        Label.__init__(self, master, text=text, **kwargs)
        self.indicator = text

    def show_indicator(self):
        self.config(text=self.indicator)

    def hide_indicator(self):
        self.config(text="")

    def is_required(self) -> bool:
        return self.cget("text") == self.indicator

    @classmethod
    def default_colorscheme(cls):
        return { **Label.default_colorscheme(), **cls.indicator_colorscheme }


class FormLabel(Container):
    """Custom form label with support to required `*` indicator."""

    def __init__(self,
        master: tk.Misc,
        *,
        text: str,
        required: bool,
        options: Mapping[str, Any] | None = None,
        **kwargs,
    ):
        Container.__init__(self, master, **kwargs)
        self.text = Label(self, text=text, **(options or {}))
        self.asterisk = Asterisk(self)
        self.required = required

    @property
    def required(self) -> bool:
        return self.asterisk.is_required()

    @required.setter
    def required(self, value: bool):
        if value:
            self.asterisk.show_indicator()
        else:
            self.asterisk.hide_indicator()

    def setup(self):
        self.text.pack(side="left")
        self.asterisk.pack(side="left")


class FormErrorLabel(Label):
    """Custom form error label."""

    def show(self, error: str):
        self.config(text=error)

    def clear(self):
        self.config(text="")

    @classmethod
    def default_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return { **Label.default_colorscheme(), "foreground": "red" }
