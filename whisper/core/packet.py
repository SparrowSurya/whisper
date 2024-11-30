import abc
import struct
import logging
from enum import IntEnum, auto
from typing import Awaitable, Callable, Type, Tuple, Dict


__all__ = (
    "PacketKind",
    "Packet",
    "PacketRegistery",
    "PacketV1",
)


logger = logging.getLogger(__name__)


class Packet(abc.ABC):
    """Base Packet class. Child class must inherit the class for sending
    data across the stream."""

    @classmethod
    @abc.abstractmethod
    def get_version(cls) -> int:
        """Packet version."""

    @classmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]):
        """Read (async) the packet from stream.
        
        NOTE: Make sure that reader do not provides empty bytes.
        """
        version = struct.unpack("B", await reader(1))[0]
        handler_cls = PacketRegistery.get(version)
        return await handler_cls.from_stream(reader)

    @abc.abstractmethod
    def to_stream(self) -> bytes:
        """Convert the packet into bytes.

        NOTE: This part should be placed at the beginning by the child
        class. This is for automatic detection of correct packet version.
        """
        return struct.pack("B", self.get_version())

    @abc.abstractmethod
    def get_data(self) -> bytes:
        """Data carried by the packet."""


class PacketRegistery:
    """Manages the packet versions."""

    _handlers: Dict[int, Type[Packet]] = {}

    @staticmethod
    def register(handler: Type[Packet]) -> Type[Packet]:
        """Decorator to register a packet.

        Usage:
        >>> @PacketRegistery.register
        >>> class PacketV1(Packet):
        >>>     ...
        """
        if not issubclass(handler, Packet):
            msg = f"{handler!s} must be subclass of `Packet`"
            logger.error(msg)
            raise ValueError(msg)

        version = handler.get_version()
        if version in PacketRegistery._handlers:
            msg = f"Packet v{version} is registered"
            logger.error(msg)
            raise TypeError(msg)

        PacketRegistery._handlers[version] = handler
        logger.debug(f"Packet v{version} registered")
        return handler

    @classmethod
    def get(cls, version: int) -> Type[Packet]:
        """Get `Packet` class for the version."""
        try:
            handler = cls._handlers[version]
        except KeyError as error:
            logger.error(error)
            raise
        return handler

    @classmethod
    def supported_versions(cls) -> Tuple[int, ...]:
        """Provides supported packet versions."""
        return tuple(cls._handlers.keys())


class PacketKind(IntEnum):
    """Defines the kind of packet."""

    EXIT = 0
    """Client is closing the connection."""

    INIT = auto()
    """Initialise the connection with server."""

    ACK = auto()
    """Acknowledgement about packet from server."""

    def __str__(self):
        return self.name.lower().replace("_", "-")


@PacketRegistery.register
class PacketV1(Packet):
    """Packet Version 1.

    Structure:
    ```
      1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    |     Version     |      kind       |            Data length            |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    |            Data (<= 64KB)...                                          |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    ```
    """

    @classmethod
    def get_version(cls) -> int:
        """Packet version."""
        return 1

    def __init__(self, kind: PacketKind, data: bytes):
        """
        Arguments:
        * kind - kind of the packet
        * data - data to be transferred

        NOTE - data size should not exceed 64KB.
        """
        self.kind = kind
        self.data = data

    def get_data(self) -> bytes:
        """The data carried by the packet."""
        return self.data

    @classmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]):
        """Read packet from the stream."""
        kind = PacketKind(struct.unpack("B", await reader(1))[0])
        length = struct.unpack("H", await reader(2))[0]
        data = await reader(length)
        return cls(kind, data)

    def to_stream(self) -> bytes:
        """Convert packet into stream of bytes."""
        if len(self.data) > self.MAX_DATA_SIZE:
            msg = f"Packet data length exceeded, {(len(self.data)/1024):.1}KB > 64KB"
            logger.error(msg)
            raise ValueError(msg)

        version = super().to_stream()
        kind = struct.pack("B", self.kind)
        length = struct.pack("H", len(self.data))
        return version + kind + length + self.data

    @property
    def MAX_DATA_SIZE(self) -> int:
        """Maximum size of payload data supported."""
        return 0xFFFF_FFFF_FFFF_FFFF

    def __str__(self):
        return str(self.data)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, type(self))
            and self.get_version() == other.get_version()
            and self.kind == other.kind
            and self.data == other.data
        )

    def __repr__(self):
        return f"<Packet-v{self.get_version()}: {self.kind!s}>"
