"""
This module provides form widget.
"""

import tkinter as tk
from typing import Dict, Set, Any, Callable

from .. import Container
from .base import FormInput


class Form(Container):
    """Custom form widget."""

    def __init__(self,
        master: tk.Misc,
        submit_cb: Callable[[Dict[str, Any]], None],
        **kwargs,
    ):
        Container.__init__(self, master, **kwargs)
        self.inputs: Set[FormInput] = set()
        self._submit_cb = submit_cb

    def set_initial_values(self, **values: Any):
        """Set inital values."""
        for field in self.inputs:
            self.field.initial_value = values[field.name]

    def validate(self) -> bool:
        """Validates input fields."""
        return all(widget.validate() for widget in self.inputs)

    def collect_values(self) -> Dict[str, Any]:
        """Read values from input fields."""
        return {widget.name: widget.value for widget in self.inputs}

    def submit_form(self):
        """Submit form if validation success."""
        if self.validate():
            values = self.collect_values()
            self._submit_cb(**values)

    def reset(self):
        """Resets form input."""
        for widget in self.inputs:
            widget.reset(use_initial_value=True)

    def cancel(self):
        """Cancel the form submission."""
