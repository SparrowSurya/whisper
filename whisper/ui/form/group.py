"""
This module provides form input groups.
"""

from typing import Sequence

from .. import Container
from .input import AbstractInputField, TextField
from .label import FormLabel, FormErrorLabel
from whisper.typing import (
    Misc as _Misc,
    Validator as _Validator,
)


class TextFieldGroup(Container, AbstractInputField):
    """Custom form text input widget with error label."""

    def __init__(self,
        master: _Misc,
        *,
        label: str,
        name: str,
        required: str,
        initial_value: str = "",
        validators: Sequence[_Validator] | None = None,
        **kwargs,
    ):
        Container.__init__(self, master, **kwargs)

        self.label = FormLabel(self, text=label, required=required)
        self.input = TextField(self, name=name, initial_value=initial_value,
                               validators=validators)
        self.error = FormErrorLabel(self, justify="w")

        AbstractInputField.__init__(self, name=name, initial_value=initial_value,
                                    validators=validators)

    def setup(self):
        self.label.label.config(justofy="W")
        self.label.setup()
        self.input.setup()
        self.error.setup()

    @property
    def name(self) -> str:
        return self.input.name

    def set_value(self, value: str):
        return self.input.set_value(value)

    def get_value(self) -> str:
        return self.input.get_value()

    def enable(self) -> bool:
        return self.input.enable()

    def disable(self) -> bool:
        return self.input.disable()

    def set_error(self, error):
        self.input.set_error(error)
        self.error.show_error(error)

    def unset_error(self):
        self.input.unset_error()
        self.error.clear_error()

    def validate(self) -> bool:
        return self.input.validate()

    def reset(self, value: str | None = None):
        self.input.reset("" if value is None else value)
