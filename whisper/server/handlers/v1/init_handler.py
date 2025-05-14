"""
This module provides init packet-v1 request handler.
"""

import re
import random
import string
from typing import Tuple

from whisper.packet.v1 import PacketType, InitV1Packet, Status
from whisper.server.connection import ConnHandle
from .base import RequestV1Handler


class InitV1Handler(RequestV1Handler):

    username_regex = re.compile("^[a-zA-Z0-9_@-]{3, 15}$")
    username_error = {
        "pattern": "username must consist of alphanumeric characters and '_', '-', '@' symbols only",
        "length": "username should have length between 3 and 15",
    }

    charset = string.ascii_letters + string.digits
    keylen = 8

    @staticmethod
    def packet_type() -> PacketType:
        return InitV1Packet.packet_type()

    @staticmethod
    def unique_key():
        return InitV1Packet.unique_key()

    def handle(self, conn: ConnHandle, *args, username: str, **kwargs):
        username_or_msg, success = self.validate_username(username)
        if not success:
            packet = InitV1Packet.response(
                status=Status.VALIDATION_ERROR,
                message=username_or_msg,
                error="validation",
                field="username")
            return [(packet, [conn])]

        conn.serve = True
        packet = InitV1Packet.response(
            status=Status.SUCCESS,
            username=username_or_msg,
            key=self.create_unique_key())
        return [(packet, [conn])]

    def validate_username(self, username: str) -> Tuple[str, bool]:
        """If success provides username otherwise error message."""
        username = username.strip()
        if len(username) not in range(3, 16):
            return self.username_error["length"], False
        if self.username_regex.fullmatch(username):
            return username, True
        return self.username_error["pattern"], False

    def create_unique_key(self) -> str:
        """Provide fixed length unique key."""
        return "".join(random.choice(self.charset) for _ in range(self.keylen))
