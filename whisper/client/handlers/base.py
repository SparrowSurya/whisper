"""
This module provide base response handler for client.
"""

from typing import Any

from whisper.handler import AbstractPacketHandler


class ResponsePacketHandler(AbstractPacketHandler):
    """
    Response packet handler for client. It handles response packet from server and
    performs required actions on client side.
    """

    def __init__(self, client: Any):
        super().__init__(client)
        self.client = self.app
