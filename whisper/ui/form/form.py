"""
This module provides form widget.
"""

from typing import Mapping, Any, Set

from .input import AbstractInputField
from whisper.typing import (
    FormSubmitCmd as _FormSubmitCmd,
    FormCancelCmd as _FormCancelCmd,
    FormResetCmd as _FormResetCmd,
)


class BaseForm:
    """Base form component."""

    def __init__(self,
        submit_cb: _FormSubmitCmd,
        cancel_cb: _FormCancelCmd | None = None,
        reset_cb: _FormResetCmd | None = None,
    ):
        self._submit_cb = submit_cb
        self._cancel_cb = cancel_cb
        self._reset_cb = reset_cb
        self.inputs: Set[AbstractInputField] = set()

    def setup(self,
        values: Mapping[str, Any] | None = None,
        errors: Mapping[str, Any] | None = None,
    ):
        """setup and configure widgets."""
        for inp in self.inputs:
            value = values.get(inp._name, None) if values else None
            if value is not None:
                inp.set_value(value=value)
            error = errors.get(inp._name, None) if errors else None
            if error is not None:
                inp.set_error(error=error)

    def values(self) -> Mapping[str, Any]:
        """Provides the values from inputs."""
        return {inp._name: inp.get_value() for inp in self.inputs}

    def validate(self) -> bool:
        """Validate all inputs."""
        return all(inp.validate() for inp in self.inputs)

    def submit_form(self):
        """Submit the form."""
        if self.validate():
            values = self.values()
            self._submit_cb(**values)

    def cancel_form(self):
        """Cancel the form."""
        if callable(self._cancel_cb):
            self._cancel_cb()

    def reset_form(self):
        """Reset form inputs."""
        values = self._reset_cb() if callable(self._reset_cb) else None
        for inp in self.inputs:
            value = values.get(inp._name, None) if values else None
            inp.reset(value=value)
