"""
This module provides connection initilization form dialog.
"""

from typing import Callable, Dict, Any

from whisper.ui import Container, Dialog
from whisper.ui.form import BaseForm, FormSubmitButton, TextFieldGroup, validators
from whisper.typing import (
    Misc as _Misc,
    FormSubmitCmd as _FormSubmitCmd,
)


class ConnInitForm(Container, BaseForm):
    """Form component for connection initilization.

    Inputs:
    * username
    """

    def __init__(self, master: _Misc, submit_cb: _FormSubmitCmd, **kwargs):
        Container.__init__(self, master, width=200, **kwargs)
        BaseForm.__init__(self, submit_cb=submit_cb)

        self.username = TextFieldGroup(self, name="username", label="Username",
                                       required="*", validators=[validators.required])
        self.submit = FormSubmitButton(self, form=self, text="Submit", borderwidth=1, border=1)

        self.inputs.add(self.username)

    def setup(self):
        self.username.setup()
        self.submit.setup()
        self.username.label.pack(fill="x", pady=(8, 4))
        self.username.input.pack(fill="x", pady=(4, 0))
        self.username.error.pack(side="left", pady=(0, 8))
        self.username.pack(fill="x")
        self.submit.pack(side="right")


class ConnInitFormDialog(Dialog):

    def __init__(self, master: _Misc, submit_cb: Callable[[Dict[str, Any]], None]):
        super().__init__(master)
        self.app = master.app
        self.title("Connect to server ...")
        self.minsize(260, 120)

        self.form = ConnInitForm(self, submit_cb, padx=16, pady=16)
        self.form.pack(fill="x")
        self.set_theme(self.app.setting.theme)

    def setup(self):
        super().setup()
        self.form.setup()
