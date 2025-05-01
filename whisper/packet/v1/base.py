"""
This modules provides packet version 1 and related objects.
"""

import struct
from enum import IntEnum, auto
from functools import cached_property
from typing import Tuple, Dict, Type, Awaitable, Callable

from whisper.packet import Packet, PacketRegistery


__all__ = (
    "PacketType",
    "Status",
    "PacketV1",
    "PacketV1Registery",
)


class PacketType(IntEnum):
    """Packet types for `PacketV1`."""

    EXIT = 0
    INIT = auto()
    MESSAGE = auto()


class Status(IntEnum):
    """Response status codes."""

    SUCCESS = 0
    VALIDATION_ERROR = auto()


@PacketRegistery.register
class PacketV1(Packet):
    """
    Abstract PacketV1 packet structure. This class provides base for all kinds of child
    packet implementation belongs to version 1. It also supports status code for server
    response.

    Structure:
    ```
      1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    |     Version     |   PacketType    |            Data length            |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    | Status | 0b0000 |                Data (length bytes) ...              |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    ```

    This class is supposed to be inherited by child class to provide custom packets.
    """

    @staticmethod
    def version() -> int:
        """Packet version."""
        return 1

    def __init__(self, type_: PacketType, data: bytes, status: Status):
        super().__init__(data)
        self.type = type_
        self.status = status

    @classmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]):
        """Construct packet from the stream."""
        type_ = PacketType(struct.unpack("B", await reader(1))[0])
        length = struct.unpack("H", await reader(2))[0]
        status = Status(struct.unpack("B", await reader(1))[0])
        data = await reader(length)
        handler = PacketV1Registery.get_packet_cls(type_)
        return handler(type_, data, status)

    def to_stream(self) -> bytes:
        """Convert packet into stream of bytes."""
        size_limit = self.data_size_limit
        data_size = len(self.data)
        if data_size > size_limit:
            raise ValueError(
                f"data size limit exceeded: limit={(size_limit/1024):.0}KB "
                f"got {(data_size/1024):.2}KB"
            )

        version = super().to_stream()
        type_ = struct.pack("B", self.type)
        length = struct.pack("H", len(self.data))
        status = struct.pack("B", (self.status & 0x0F) << 4)
        return version + type_ + length + status + self.data

    @cached_property
    def data_size_limit(self) -> int:
        """Maximum bytes of data supported."""
        metadata = 1 + 1 + 2 + 1
        return 0xFFFF - metadata

    @staticmethod
    def packet_type() -> PacketType:
        """Child class must implement this to define the type they handle."""
        raise NotImplementedError

    @classmethod
    def create(cls, data: bytes, status: Status = Status.SUCCESS):
        return cls(type_=cls.packet_type(), data=data, status=status,)

    @classmethod
    def request(cls, *args, **kwargs):
        """This must be implemented by child class."""
        raise NotImplementedError

    @classmethod
    def response(cls, *args, **kwargs):
        """This must be implemented by child class."""
        raise NotImplementedError

    def __repr__(self) -> str:
        name = type(self).__name__
        version = self.version()
        return f"<{name}v{version}>"


class PacketV1Registery:
    """Manages the packetv1 handlers. Do not instantiate this class."""

    _handlers: Dict[PacketType, Type[PacketV1]] = {}
    """Maps packet type against their handlers."""

    @staticmethod
    def validate(handler: Type[PacketV1]):
        """Performs validation checks on packet"""
        if not issubclass(handler, PacketV1):
            msg = f"{handler.__name__} must be subclass of `PacketV1`"
            raise ValueError(msg)

        type = handler.packet_type()
        if PacketV1Registery._handlers.get(type) is not None:
            msg = f"{handler.__name__} is already registered"
            raise ValueError(msg)

    @staticmethod
    def register(handler: Type[PacketV1]) -> Type[PacketV1]:
        """
        Use this as decorator to register a packet type handler.

        Usage:
        >>> @PacketTypeRegistery.register
        >>> class MyPacket(PacketV1):
        >>>     ...
        """
        PacketV1Registery.validate(handler)
        PacketV1Registery._handlers[handler.packet_type()] = handler
        return handler

    @staticmethod
    def get_packet_cls(type: PacketType) -> Type[PacketV1]:
        """Get packet class for the packet version."""
        return PacketV1Registery._handlers[type]

    @staticmethod
    def registered_versions() -> Tuple[PacketType, ...]:
        """Provides registered packet versions."""
        return tuple(PacketV1Registery._handlers.keys())
