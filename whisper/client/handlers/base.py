"""
This module provide abstract pacekt-v1 response handler for client.
"""

from typing import Any

from whisper.handler import PacketV1Handler


class PacketV1ResponseHandler(PacketV1Handler):
    """
    Response packet-v1 handler for client. It handles response packet from server and
    performs required actions on client.
    """

    def __init__(self, client: Any):
        super().__init__(client)
        self.client = self.app
