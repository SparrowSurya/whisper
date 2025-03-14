"""
This modules provies the packet used for communication to the server.
"""

import abc
import struct
import logging
from enum import IntEnum
from functools import cached_property
from typing import Awaitable, Callable, Type, Tuple, Dict


__all__ = (
    "PacketKind",
    "Packet",
    "PacketRegistery",
    "PacketV1",
)


logger = logging.getLogger(__name__)


class Packet(abc.ABC):
    """
    Abstract Packet class. It handles the packet being created from
    stream of bytes and the required packet version. Implement this
    to customise the packet structure.
    """

    def __init__(self, data: bytes = b""):
        self.data = data

    @classmethod
    @abc.abstractmethod
    def get_version(cls) -> int:
        """Packet version."""

    @classmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]) -> "Packet":
        """
        Creates the packet from asynchronous stream of bytes. It reads
        the first byte from stream to know the packet version then call
        to respective packet's classmethod is made to further read the
        bytes to parse the data as per their format.

        NOTE:
        1. Make sure that reader do not provides empty bytes.
        2. Packet version must be registered in `PacketRegistery`.
        """
        version = struct.unpack("B", await reader(1))[0]
        handler_cls = PacketRegistery.get_handler(version)
        return await handler_cls.from_stream(reader)

    @abc.abstractmethod
    def to_stream(self) -> bytes:
        """Converts the packet into stream of bytes.

        NOTE: This data must be placed before the data being sent by
        the packet itself.
        """
        return struct.pack("B", self.get_version())

    def __repr__(self):
        """Simple packet representation."""
        return f"<Packet-v{self.get_version()}>"


class PacketRegistery:
    """
    Manages the packet versions and their respective handlers.

    NOTE: Usethis directly instead creating an instance.
    """

    _handlers: Dict[int, Type[Packet]] = {}
    """Maps version against their handlers."""

    @staticmethod
    def register(handler: Type[Packet]) -> Type[Packet]:
        """
        Use this as decorator to register a packet. Since single byte
        is used to store the packet version it cannot exceed `255` and
        `0` is not allowed as version.

        Usage:
        >>> @PacketRegistery.register
        >>> class PacketV1(Packet):
        >>>     ...
        """
        assert issubclass(handler, Packet), (
            f"{handler.__name__} must be subclass of `Packet`"
        )
        version = handler.get_version()

        assert version in range(1, 256),(
            f"Version number {version} is not allowed!"
        )
        assert version not in PacketRegistery._handlers, (
            f"Packet v{version} is already registered"
        )

        PacketRegistery._handlers[version] = handler
        logger.debug(f"Packet v{version} registered")
        return handler

    @classmethod
    def get_handler(cls, version: int) -> Type[Packet]:
        """Get `Packet` class for the version."""
        try:
            handler = cls._handlers[version]
        except KeyError as error:
            logger.error(error)
            raise
        return handler

    @classmethod
    def registered_versions(cls) -> Tuple[int, ...]:
        """Provides registered packet versions."""
        return tuple(cls._handlers.keys())


# TODO - what kind of packets are required?
class PacketKind(IntEnum):
    """Defines the kind of packet."""

    # EXIT = 0
    # """Client is closing the connection."""

    # INIT = auto()
    # """Initialise the connection with server."""

    # ACK = auto()
    # """Acknowledgement about packet from server."""

    # def __str__(self):
    #     return self.name.lower().replace("_", "-")


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
        super().__init__(data)
        self.kind = kind

    @classmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]):
        """Read packet from the stream."""
        kind = PacketKind(struct.unpack("B", await reader(1))[0])
        length = struct.unpack("H", await reader(2))[0]
        data = await reader(length)
        return cls(kind, data)

    def to_stream(self) -> bytes:
        """Convert packet into stream of bytes."""
        size_limit = self.data_size_limit
        data_size = len(self.data)
        if data_size < size_limit:
            msg = (
                f"{self.__class__.__name__} data size exceeded: "
                f"size={(data_size/1024):.3}KB "
                f"Limit={(size_limit/1024):.0}KB"
            )
            logger.error(msg)
            raise ValueError(msg)

        version = super().to_stream()
        kind = struct.pack("B", self.kind)
        length = struct.pack("H", len(self.data))
        return version + kind + length + self.data

    @cached_property
    def data_size_limit(self) -> int:
        """Maximum bytes of data supported."""
        return 0xFFFF_FFFF_FFFF_FFFF - (8+8+16)
