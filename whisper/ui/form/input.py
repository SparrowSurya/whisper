"""
This module provides form inputs.
"""

import abc
from typing import Generic, TypeVar, Sequence, Mapping, Any

from .. import Input
from whisper.typing import (
    Misc as _Misc,
    Validator as _Validator,
    InputColorAttr as _ColorAttr,
    PaletteOpts as _PaletteOpts,
)


_V = TypeVar("_V")
_E = TypeVar("_E")


class AbstractInputField(abc.ABC, Generic[_V]):
    """Abstract input widget."""

    def __init__(self,
        name: str,
        initial_value: _V | None = None,
        validators: Sequence[_Validator] | None = None,
    ):
        self._name = name
        self._validators = validators

        if initial_value is not None:
            self.set_value(initial_value)

    @property
    def name(self) -> str:
        """Provides name of input field."""
        return self._name

    @abc.abstractmethod
    def set_value(self, value: _V):
        """Write the input value into widget."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_value(self) -> _V:
        """Read the input value from widget."""
        raise NotImplementedError

    @abc.abstractmethod
    def enable(self):
        """Enable the widget to take user input."""
        raise NotImplementedError

    @abc.abstractmethod
    def disable(self):
        """Disable widget to prevent user input."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_error(self, error: _E):
        """Show error on input widget."""
        raise NotImplementedError

    @abc.abstractmethod
    def unset_error(self):
        """Clear error on input widget."""
        raise NotImplementedError

    def validate(self) -> bool:
        """validate widget input value."""
        for validator in self._validators or []:
            success, value = validator(self.get_value())
            if not success:
                self.set_error(value)
                return False
        return True

    def reset(self, value: _V | None = None):
        """Reset form input."""
        if value is not None:
            self.set_value(value)


class TextField(Input, AbstractInputField):
    """Custom form text input widget with error indication support."""

    use_theme_ref = True

    def __init__(self,
        master: _Misc,
        *,
        name: str,
        initial_value: str = "",
        validators: Sequence[_Validator] | None = None,
        **kwargs,
    ):
        Input.__init__(self, master, **kwargs)
        AbstractInputField.__init__(self, name=name, initial_value=initial_value,
                                    validators=validators)

    def set_value(self, value: str):
        Input.set_value(self, value)

    def get_value(self) -> str:
        return Input.get(self)

    def enable(self):
        Input.config(self, state="normal")
        if self.use_theme_ref and self.theme_ref is not None:
            self.set_theme_self(self.theme_ref(), "default") # FIXME: can be `None`

    def disable(self):
        Input.config(self, state="disabled")
        if self.use_theme_ref and self.theme_ref is not None:
            self.set_theme_self(self.theme_ref(), "disabled") # FIXME: can be `None`

    def set_error(self, error: Any):
        if self.use_theme_ref and self.theme_ref is not None:
            self.set_theme_self(self.theme_ref(), "invalid") # FIXME: can be `None`

    def unset_error(self):
        if self.use_theme_ref and self.theme_ref is not None:
            self.set_theme_self(self.theme_ref(), "default") # FIXME: can be `None`

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
