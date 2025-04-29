"""
This modules provies the packet used for communication between client and server.
"""

import abc
import struct
from typing import Any, Awaitable, Callable, Dict, Tuple, Type


class Packet(metaclass=abc.ABCMeta):
    """
    Abstract Packet class. It handles the packet being created from stream of bytes
    and the required packet version. Implement this to customise the packet structure.

    It depends upon `PacketRegistery` to determine handler.
    """

    def __init__(self, data: bytes = b""):
        """Stores payload data that is being sent/received."""
        self.data = data

    @staticmethod
    @abc.abstractmethod
    def version() -> int:
        """Provides the packet version."""
        msg = "Child class must define their unique packet version."
        raise NotImplementedError(msg)

    @classmethod
    @abc.abstractmethod
    async def from_stream(cls, reader: Callable[[int], Awaitable[bytes]]):
        """
        Creates the packet from asynchronous stream of bytes. It reads the first byte
        from stream to know the packet version then call to respective packet's
        classmethod is made to further read the bytes to parse the data as per its
        format.

        NOTE:
        1. Reader should not provides empty bytes.
        2. Packet version must be registered in `PacketRegistery`.

        The child class needs to implement this method for further reading as per its
        structure.
        """
        version = struct.unpack("B", await reader(1))[0]
        packet = PacketRegistery.get_packet_cls(version)
        return await packet.from_stream(reader)

    @classmethod
    @abc.abstractmethod
    def create(cls, *args: Any, **kwargs: Any):
        """Create packet from the arguments."""

    @classmethod
    @abc.abstractmethod
    def request(cls, *args: Any, **kwargs: Any):
        """Create request packet."""

    @classmethod
    @abc.abstractmethod
    def response(cls, *args: Any, **kwargs: Any):
        """Create response packet."""

    @abc.abstractmethod
    def to_stream(self) -> bytes:
        """Converts the packet into stream of bytes. This data must be placed before
        the data being sent by the packet itself."""
        return struct.pack("B", self.version())

    @abc.abstractmethod
    def content(self) -> Any:
        """Get the contents from data."""

    def __repr__(self):
        return f"<Packet-v{self.version()}>"


class PacketRegistery:
    """
    Manages the packet versions and their respective handlers. Not all versions are
    allowed (see `version_allowed`). Use the class directly instead creating instance.
    """

    _packets: Dict[int, Type[Packet]] = {}
    """Maps version against their handlers."""

    @staticmethod
    def version_allowed(version: int):
        """Know if version is allowed or not."""
        return version in range(1, 256)

    @staticmethod
    def validate(packet: Type[Packet]):
        """Performs validation checks on packet"""
        if not issubclass(packet, Packet):
            msg = f"{packet.__name__} must be subclass of `Packet`"
            raise ValueError(msg)

        version = packet.version()
        if not PacketRegistery.version_allowed(version):
            msg = f"Version number {version} is not allowed!"
            raise ValueError(msg)

        if PacketRegistery._packets.get(version) is not None:
            msg = f"Packet v{version} is already registered"
            raise ValueError(msg)

    @staticmethod
    def register(packet: Type[Packet]) -> Type[Packet]:
        """Use this as decorator to register a packet.

        Usage:
        >>> @PacketRegistery.register
        >>> class PacketV1(Packet):
        >>>     ...
        """
        PacketRegistery.validate(packet)
        PacketRegistery._packets[packet.version()] = packet
        return packet

    @staticmethod
    def get_packet_cls(version: int) -> Type[Packet]:
        """Get packet class for the packet version."""
        return PacketRegistery._packets[version]

    @staticmethod
    def registered_versions() -> Tuple[int, ...]:
        """Provides registered packet versions."""
        return tuple(PacketRegistery._packets.keys())
