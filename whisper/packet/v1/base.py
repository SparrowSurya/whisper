"""
This modules provides the `PacketV1` abstract class, `PacketType` and its registery
object.
"""

import abc
import struct
from enum import IntEnum, auto
from functools import cached_property
from typing import Awaitable, Callable, Any

from whisper.packet import Packet, PacketRegistery


__all__ = (
    "PacketType",
    "PacketV1",
)


class PacketType(IntEnum):
    """Packet types for `PacketV1`."""

    EXIT = 0
    INIT = auto()
    MESSAGE = auto()


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
    |  Code  | 0b0000 |                Data (length bytes) ...              |
    + - - - - - - - - + - - - - - - - - + - - - - - - - - + - - - - - - - - +
    ```

    Use code value zero for request packet and non zero 4 bit int for response packet.
    """

    @classmethod
    def version(cls) -> int:
        """Packet version."""
        return 1

    def __init__(self, type_: PacketType, data: bytes, code: int):
        super().__init__(data)
        self.type = type_
        self.code = code

    @classmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]):
        """Construct packet from the stream."""
        type_ = PacketType(struct.unpack("B", await reader(1))[0])
        length = struct.unpack("H", await reader(2))[0]
        code = struct.unpack("B", await reader(1))[0]
        data = await reader(length)
        return cls(type_, data, code)

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
        code = struct.pack("B", (self.code & 0x0F) << 4)
        return version + type_ + length + code + self.data

    @cached_property
    def data_size_limit(self) -> int:
        """Maximum bytes of data supported."""
        metadata = 1 + 1 + 2 + 1
        return 0xFFFF - metadata

    @classmethod
    @abc.abstractmethod
    def packet_type(cls) -> PacketType:
        """Child class must implement this to define the type they handle."""

    @classmethod
    def create(cls, data: bytes, code: int = 0):
        return cls(type_=cls.packet_type(), data=data, code=code,)
