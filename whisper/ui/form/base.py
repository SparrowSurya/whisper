"""
This module provides base classes for form.
"""

import abc
from enum import StrEnum, auto
from typing import Any


class FormInput(abc.ABC):
    """Abstract custom form input."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of the form input field. Do not confuse it with tkinter widget name
        property."""

    @property
    @abc.abstractmethod
    def initial_value(self, value: Any):
        """Set initial value in the input."""

    @property
    @abc.abstractmethod
    def value(self) -> Any:
        """Provide the input value."""

    @property
    @abc.abstractmethod
    def disable(self) -> bool:
        """Provide input disabled state status."""

    @abc.abstractmethod
    def auto_validate(self, **kwargs: Any) -> bool:
        """Automatically trigerred (if vcmd provided) based on validation type."""

    @abc.abstractmethod
    def validate(self, effect: bool = True) -> str | None:
        """Validate the form and return validation success."""

    @abc.abstractmethod
    def show_invalid(self, error: str = ""):
        """Show the invalid indicator on input."""

    @abc.abstractmethod
    def clear_invalid(self):
        """Clear the invalid indication if there."""

    @abc.abstractmethod
    def reset(self, use_initial_value: bool = False):
        """Reset the form input."""


class FormActionType(StrEnum):
    """Form action types."""

    SUBMIT = auto()
    CANCEL = auto()
    RESET = auto()


class FormAction(abc.ABC):
    """Abstract form action class."""

    @classmethod
    @abc.abstractmethod
    def action_type(cls) -> FormActionType:
        """Know the kind of action is being done."""
