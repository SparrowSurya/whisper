"""
This module provides form action buttons.
"""

import tkinter as tk

from .. import Button
from .base import Form, FormAction, FormActionType


class FormSubmit(Button, FormAction):
    """Form save action button."""

    def __init__(self, master: tk.Misc, form: Form, **kwargs):
        if "command" in kwargs:
            wid = type(self).__name__
            raise TypeError(
                f"{wid} don't supports `validatecommand` use `validate` method")
        Button.__init__(self, master, command=form.submit, **kwargs)
        self.form = form

    @classmethod
    def action_type(self) -> FormActionType:
        return FormActionType.SUBMIT

    @classmethod
    def default_colorscheme(cls):
        return {
            **Button.default_colorscheme(),
            "foreground": "base",
            "background": "green",
            "activeforeground": "base",
            "activebackground": "mauve",
            "disabledforeground": "overlay0",
            "disabledbackground": "surface1",
        }


class FormCancel(Button, FormAction):
    """Form cancel action button."""

    def __init__(self, master: tk.Misc, form: Form, **kwargs):
        if "command" in kwargs:
            wid = type(self).__name__
            raise TypeError(
                f"{wid} don't supports `validatecommand` use `validate` method")
        Button.__init__(self, master, command=form.cancel, **kwargs)
        self.form = form

    @classmethod
    def action_type(self) -> FormActionType:
        return FormActionType.SUBMIT

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


class FormReset(Button, FormAction):
    """Form reset action button."""

    def __init__(self, master: tk.Misc, form: Form, **kwargs):
        if "command" in kwargs:
            wid = type(self).__name__
            raise TypeError(
                f"{wid} don't supports `validatecommand` use `validate` method")
        Button.__init__(self, master, command=form.reset, **kwargs)
        self.form = form

    @classmethod
    def action_type(self) -> FormActionType:
        return FormActionType.SUBMIT

    @classmethod
    def default_colorscheme(cls):
        return {
            **Button.default_colorscheme(),
            "foreground": "base",
            "background": "yellow",
            "activeforeground": "base",
            "activebackground": "peach",
            "disabledforeground": "overlay0",
            "disabledbackground": "surface1",
        }
