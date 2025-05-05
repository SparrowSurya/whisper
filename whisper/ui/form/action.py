"""
This module provides form action buttons.
"""

import abc
import tkinter as tk

from .. import Button
from .form import BaseForm
from whisper.typing import (
    Misc as _Misc,
    FormActionType as _FormActionType
)


class FormAction(abc.ABC):
    """Abstract form action class."""

    def __init__(self, form: BaseForm):
        self._form = form

    @staticmethod
    @abc.abstractmethod
    def action_type() -> _FormActionType:
        """Know the kind of action is being done."""


class FormSubmitButton(Button, FormAction):
    """Button triggering form submit."""

    def __init__(self, master: _Misc, *, form: BaseForm, **kwargs):
        if "command" in kwargs:
            wid = type(self).__name__
            raise TypeError(f"{wid} don't supports `command` argument")
        Button.__init__(self, master, command=form.submit_form, **kwargs)
        FormAction.__init__(self, form=form)

    @staticmethod
    def action_type() -> _FormActionType:
        return "submit"

    @classmethod
    def default_colorscheme(cls):
        return {
            **Button.default_colorscheme(),
            "foreground": "base",
            "background": "mauve",
            "activeforeground": "base",
            "activebackground": "overlay0",
            "disabledforeground": "overlay0",
        }


class FormCancelButton(Button, FormAction):
    """Form cancel action button."""

    def __init__(self, master: tk.Misc, form: BaseForm, **kwargs):
        if "command" in kwargs:
            wid = type(self).__name__
            raise TypeError(f"{wid} don't supports `command` argument")
        Button.__init__(self, master, command=form.cancel_form, **kwargs)
        FormAction.__init__(self, form=form)

    @staticmethod
    def action_type() -> _FormActionType:
        return "cancel"

    @classmethod
    def default_colorscheme(cls):
        return {
            **Button.default_colorscheme(),
            "foreground": "base",
            "background": "red",
            "activeforeground": "base",
            "activebackground": "flamingo",
            "disabledforeground": "overlay0",
            "disabledbackground": "surface1",
        }


class FormResetButton(Button, FormAction):
    """Form reset action button."""

    def __init__(self, master: tk.Misc, form: BaseForm, **kwargs):
        if "command" in kwargs:
            wid = type(self).__name__
            raise TypeError(f"{wid} don't supports `command` argument")
        Button.__init__(self, master, command=form.reset_form, **kwargs)
        FormAction.__init__(self, form=form)

    @staticmethod
    def action_type() -> _FormActionType:
        return "reset"

    @classmethod
    def default_colorscheme(cls):
        return {
            **Button.default_colorscheme(),
            "foreground": "base",
            "background": "yellow",
            "activeforeground": "base",
            "activebackground": "peach",
            "disabledforeground": "overlay0",
        }
