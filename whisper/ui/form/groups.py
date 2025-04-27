"""
This module provides form input groups.
"""

import tkinter as tk
from typing import Mapping, Any

from .. import Container
from .base import FormInput
from .inputs import FormTextInput
from .labels import FormLabel, FormErrorLabel


class FormTextInputGroup(Container, FormInput):
    """Custom form text input widget with error label."""

    def __init__(self,
        master: tk.Misc,
        label: str ,
        *,
        name: str = "",
        required: bool = True,
        initial_value: str = "",
        options: Mapping[str, Any] | None = None,
        **kwargs,
    ):
        Container.__init__(self, master, **kwargs)

        text_options = {"justify": "w"}
        self.label = FormLabel(self, text=label, required=required, options=text_options)
        self.input = FormTextInput(self, name=name, required=required,
            initial_value=initial_value, **(options or {}))
        self.error = FormErrorLabel(self, justify="w")

        self.name = self.input.name
        self.required = required
        self.initial_value = self.input.initial_value
        self.value = self.input.value

    def setup(self):
        self.label.setup()
        self.input.setup()
        self.error.setup()

    @property
    def required(self) -> bool:
        return self.input.required

    @required.setter
    def required(self, value: bool):
        self.input.required = value
        self.label.required = value

    @property
    def name(self) -> str:
        return self.input.name

    @name.setter
    def name(self, value: str):
        self.input.name = value

    @property
    def initial_value(self) -> str:
        return self.input.initial_value

    @initial_value.setter
    def initial_value(self, value: str):
        self.input.initial_value = value

    @property
    def value(self) -> str:
        return self.input.value

    @value.setter
    def value(self, value: str):
        self.input.value = value

    @property
    def disable(self) -> bool:
        return self.input.disable

    @disable.setter
    def disable(self, value: bool):
        self.input.disable = value

    def auto_validate(self, **kwargs: Any) -> bool:
        return self.input.auto_validate(**kwargs)

    def validate(self) -> bool:
        return self.input.validate()

    def show_invalid(self, error):
        self.input.show_invalid(error)
        self.error.show(text=error)

    def clear_invalid(self):
        self.input.clear_invalid()
        self.error.clear()

    def reset(self, use_initial_value: bool = False):
        self.input.reset(use_initial_value)
        self.error.clear()
