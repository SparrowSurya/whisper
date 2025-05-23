"""
This module provides connection initilization form dialog.
"""

from typing import Dict

from whisper.ui import Container
from whisper.ui.form import BaseForm, FormSubmitButton, TextFieldGroup, validators
from whisper.typing import (
    Misc as _Misc,
    FormSubmitCmd as _FormSubmitCmd,
)


class ConnInitForm(Container, BaseForm):
    """Form component for connection initilization."""

    def __init__(self, master: _Misc, submit_cb: _FormSubmitCmd, **kwargs):
        Container.__init__(self, master, **kwargs)
        BaseForm.__init__(self, submit_cb=submit_cb)

        self.username = TextFieldGroup(self, name="username", label="Username",
                                       required="*", validators=[validators.required])
        self.submit = FormSubmitButton(self, form=self, text="Submit", borderwidth=1, border=1)

        self.inputs.add(self.username)

    def setup(self,
        values: Dict[str, str] | None = None,
        errors: Dict[str, str] | None = None,
    ):
        BaseForm.setup(self, values, errors)
        self.username.setup()
        self.submit.setup()
        self.username.label.pack(fill="x", pady=(8, 4))
        self.username.input.pack(fill="x", pady=(4, 0))
        self.username.error.pack(side="left", pady=(0, 8))
        self.username.pack(fill="x")
        self.submit.pack(side="right")
        self.username.focus_set()
