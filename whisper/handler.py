import abc
from typing import Any

from whisper.packet.v1 import PacketV1, PacketType


class AbstractPacketHandler(abc.ABC):
    """Abstract packet type handler class for handelling request/response packet."""

    def __init__(self, app: Any):
        self.app = app
        self.logger = self.app.logger

    @classmethod
    @abc.abstractmethod
    def packet_type(cls) -> PacketType:
        """Provides the packet type handled by class."""

    def __call__(self, packet: PacketV1) -> Any:
        """Handles the request/response packet."""
        if self.packet_type() != packet.type:
            self.logger.warning(
                f"wrong packet type: expected {self.packet_type()!s}, "
                f"got {packet.type!s}"
            )
            return None
        content = packet.content()
        return self.handle(**content)

    @abc.abstractmethod
    def handle(self, *args, **kwargs) -> Any:
        """Perform required actions."""
