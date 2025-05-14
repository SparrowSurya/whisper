"""
This module provides init packet response handler.
"""

from whisper.packet.v1 import PacketType, Status, InitV1Packet
from .base import ResponseV1Handler


class InitV1Handler(ResponseV1Handler):
    """Init packet-v1 handler implementation"""

    @staticmethod
    def packet_type() -> PacketType:
        return InitV1Packet.packet_type()

    def handle(self, /, status: Status, *, username: str, key: str = "", **kwargs):
        if status == Status.SUCCESS:
            return self.handle_success(username, key, **kwargs)

        if status == Status.VALIDATION_ERROR:
            return self.handle_validation_error(username, key, **kwargs)

    def handle_success(self, username: str, key: str, **kwargs):
        self.app.setting.data["username"] = username
        self.aoo.hide_splash_screen() # TODO
        self.app.join_global_chat() # TODO

    def handle_validation_error(self, username: str, message: str, **kwargs):
        initial_values = { "username": username }
        initial_errors = { "username": message }
        self.app.init_connection(initial_values, initial_errors) # TODO
