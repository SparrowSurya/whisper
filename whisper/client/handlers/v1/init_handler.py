"""
This module provides init packet response handler.
"""

from whisper.packet.v1 import PacketType, Status, InitV1Packet
from .base import ResponseV1Handler


class InitV1Handler(ResponseV1Handler):
    """Init packet-v1 handler implementation"""

    @staticmethod
    def unique_key() -> PacketType:
        return InitV1Packet.unique_key()

    def handle(self,
        /,
        status: Status,
        *,
        username: str = "",
        key: str = "",
        message: str = "",
        field: str = "",
        value: str = "",
        **kwargs,
    ):
        if status == Status.SUCCESS:
            print(f"{username=}, {key=}")
            return self.handle_success(username, key, **kwargs)

        if status == Status.VALIDATION_ERROR:
            return self.handle_validation_error(value, message, field, **kwargs)

    def handle_success(self, username: str, key: str, **kwargs):
        self.app.setting.data["username"] = username
        # self.aoo.hide_splash_screen() # TODO
        # self.app.join_global_chat() # TODO

    def handle_validation_error(self, value: str, message: str, field: str, **kwargs):
        values = { field: value }
        errors = { field: message }
        self.app.init_connection(values, errors)
