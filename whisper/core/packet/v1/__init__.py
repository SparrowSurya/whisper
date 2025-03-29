"""
This modules provides the `PacketV1` class.
"""

import abc
import struct
from enum import IntEnum, auto
from functools import cached_property
from typing import Awaitable, Callable, Dict, Tuple, Type

from whisper.core.packet import Packet, PacketRegistery


class PacketType(IntEnum):
    """Packet types for `PacketV1`."""

    EXIT = 0
    INIT = auto()
    MESSAGE = auto()


@PacketRegistery.register
class PacketV1(Packet):
    """
    Abstract PacketV1 packet structure. This class provides base for
    all kinds of child packet implementation belongs to version 1.

    Structure:
    ```
      1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8   1 2 3 4 5 6 7 8
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    |     Version     |   PacketType    |            Data length            |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    |                                  Data                                 |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    ```
    """

    @classmethod
    def version(cls) -> int:
        """Packet version."""
        return 1

    def __init__(self, type_: PacketType, data: bytes):
        super().__init__(data)
        self.type = type_

    @classmethod
    async def from_stream(cls,
        reader: Callable[[int], Awaitable[bytes]],
    ):
        """Construct packet from the stream."""
        type_ = PacketType(struct.unpack("B", await reader(1))[0])
        packet = PacketV1Registery.get_packet_cls(type_)
        return await packet.from_stream(reader)

    def to_stream(self) -> bytes:
        """Convert packet into stream of bytes."""
        size_limit = self.data_size_limit
        data_size = len(self.data)
        if data_size < size_limit:
            size = f"{(data_size/1024):.3}KB"
            limit = f"{(size_limit/1024):.0}KB"
            msg = f"Data size exceeded {size}/{limit}"
            raise ValueError(msg)

        version = super().to_stream()
        type_ = struct.pack("B", self.type)
        length = struct.pack("H", len(self.data))
        return version + type_ + length + self.data

    @cached_property
    def data_size_limit(self) -> int:
        """Maximum bytes of data supported."""
        return 0xFFFF - (8+8+16)

    @classmethod
    @abc.abstractmethod
    def packet_type(cls) -> PacketType:
        """
        Child class must implement this to define the type they handle.
        """


class PacketV1Registery:
    """
    Manages the packet handler for each `PacketType` and their
    respective handlers.

    Use the class directly instead creating an instance.
    """

    _handlers: Dict[PacketType, Type[PacketV1]] = {}
    """Maps packet type against their handlers."""

    @classmethod
    def validate(cls, handler: Type[PacketV1]):
        """Performs validation checks on packet"""
        if not issubclass(handler, PacketV1):
            msg = f"{handler.__name__} must be subclass of `PacketV1`"
            raise ValueError(msg)

        type_ = handler.packet_type()
        if cls._handlers.get(type_) is not None:
            msg = f"{handler.__name__} is already registered"
            raise ValueError(msg)

    @classmethod
    def register(cls, handler: Type[PacketV1]) -> Type[PacketV1]:
        """
        Use this as decorator to register a packet type handler.

        Usage:
        >>> @PacketV1Registery.register(PacketType)
        >>> class MyPacket(PacketV1):
        >>>     ...
        """
        cls.validate(handler)
        cls._handlers[handler.packet_type()] = handler
        return handler

    @classmethod
    def get_packet_cls(cls, type_: PacketType) -> Type[PacketV1]:
        """Get packet class for the packet version."""
        return cls._handlers[type_]

    @classmethod
    def registered_versions(cls) -> Tuple[PacketType, ...]:
        """Provides registered packet versions."""
        return tuple(cls._handlers.keys())


@PacketV1Registery.register
class ExitPacket(PacketV1):
    """Exit packet."""

    @classmethod
    def packet_type(cls) -> PacketType:
        return PacketType.EXIT

    @classmethod
    def create(cls, reason: str): # pylint: disable=arguments-differ
        return cls(
            type_=cls.packet_type(),
            data=reason.encode(encoding="utf-8"),
        )

    @classmethod
    async def from_stream(cls,
        reader: Callable[[int], Awaitable[bytes]],
    ):
        length = struct.unpack("H", await reader(2))[0]
        data = await reader(length)
        return cls(cls.packet_type(), data)

    def content(self) -> str:
        """Provide the exit reason message."""
        return self.data.decode(encoding="UTF-8")
