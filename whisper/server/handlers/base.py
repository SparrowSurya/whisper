"""
This module provides abstract request packet-v1 handler for server.
"""

from typing import Any

from whisper.handler import PacketV1Handler


class PacketV1RequestHandler(PacketV1Handler):
    """
    Request packet-v1 handler base class for server. It handles request from client and
    provides appropriate responses to recipients.
    """

    def __init__(self, server: Any):
        super().__init__(server)
        self.server = self.app
