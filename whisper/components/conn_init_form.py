"""
This module provides connection initilization form dialog.
"""

from typing import Callable, Dict, Any

from whisper.ui import Dialog
from whisper.ui.form import Form, FormSubmit, FormTextInputGroup
from whisper.typing import MIsc as _Misc


class ConnInitForm(Form):
    def __init__(self, master, submit_cb, **kwargs):
        super().__init__(master, submit_cb, width=200, **kwargs)

        self.username = FormTextInputGroup(self, "Username", name="username")
        self.submit = FormSubmit(self, form=self, text="Submit", borderwidth=1, border=1)

        self.inputs.add(self.username)


    def setup(self):
        self.username.setup()
        self.submit.setup()
        self.username.label.pack(fill="x", pady=(8, 4))
        self.username.input.pack(fill="x", pady=(4, 0))
        self.username.error.pack(pady=(0, 8))
        self.username.pack(fill="x")
        self.submit.pack(side="right", ipadx=16, ipady=0)


class ConnInitFormDialog(Dialog):
    def __init__(self, master: _Misc, submit_cb: Callable[[Dict[str, Any]], None]):
        super().__init__(master)
        self.app = master.app
        self.title("Connect to server ...")
        self.minsize(200, 100)

        self.form = ConnInitForm(self, submit_cb)

    def setup(self):
        super().setup()
        self.form.setup()
