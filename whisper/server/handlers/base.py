"""
This module provides base request packet handler for server.
"""

from typing import Any

from whisper.handler import AbstractPacketHandler


class RequestPacketHandler(AbstractPacketHandler):
    """
    Request packet handler base class for server. It handles request from client and
    provides appropriate responses it there.
    """

    def __init__(self, server: Any):
        super().__init__(server)
        self.server = self.app
