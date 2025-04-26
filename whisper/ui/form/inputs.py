"""
This module provides form inputs.
"""

import tkinter as tk
from typing import Mapping

from .. import Input
from .base import FormInput
from whisper.typing import (
    InputColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
)


class FormTextInput(Input, FormInput):
    """Custom form input widget with error indication support."""

    use_theme_weakref = True

    def __init__(self,
        master: tk.Misc,
        *,
        name: str = "",
        required: bool = True,
        initial_value: str = "",
        **kwargs,
    ):
        Input.__init__(self, master, **kwargs)

        self._name = name
        self._required = required
        self._initial_value = initial_value

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        self._required = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def initial_value(self) -> str:
        return self._initial_value

    @initial_value.setter
    def initial_value(self, value: str):
        self._initial_value = value

    @property
    def value(self) -> str:
        return self.get()

    @value.setter
    def value(self, value: str):
        self.delete("0", "end")
        self.insert("0", value)

    @property
    def disable(self) -> bool:
        return self.cget("state") == "disabled"

    @disable.setter
    def disable(self, value: bool):
        self.config(state="disabled" if value else "normal")
        self.set_theme_self(self.theme_weakref(), "disabled" if value else "default")

    def auto_validate(self, **kwargs) -> bool:
        if self.validate() is not None:
            self.show_invalid()
        return False

    def validate(self) -> str | None:
        if self.required and self.value.strip() == "":
            return "This field is required"
        return None

    def reset(self, use_initial_value: bool = True):
        self.clear_invalid()
        if use_initial_value and self.initial_value is not None:
            self.value = str(self.initial_value)

    def show_invalid(self, error: str = ""):
        if self.use_theme_weakref:
            self.set_theme_self(self.theme_weakref(), "invalid")

    def clear_invalid(self):
        self.set_theme_self(self.theme_weakref(), "default")

    @classmethod
    def invalid_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return {
            **Input.default_colorscheme(),
            "foreground": "danger",
            "highlightbackground": "danger",
            "highlightcolor": "danger",
        }

    @classmethod
    def disabled_colorscheme(cls) -> Mapping[_ColorAttr, _PaletteOpts]:
        return {
            **Input.default_colorscheme(),
            "foreground": "overlay0",
            "disabledforeground": "overlay0",
        }
