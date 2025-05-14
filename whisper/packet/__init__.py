"""
This modules provies the packet used for communication between client and server.
"""

import re
import abc
import struct
import logging
import pathlib
import importlib
from types import ModuleType
from typing import Any, Awaitable, Callable, Dict, List, Type, ClassVar


logger = logging.getLogger(__name__)


class Packet(abc.ABC):
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
        packet = PacketRegistery.packets[version]
        return await packet.from_stream(reader)

    @classmethod
    @abc.abstractmethod
    def create(cls, *args: Any, **kwargs: Any):
        """Create packet from the arguments."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def request(cls, *args: Any, **kwargs: Any):
        """Create request packet."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def response(cls, *args: Any, **kwargs: Any):
        """Create response packet."""
        raise NotImplementedError

    @abc.abstractmethod
    def to_stream(self) -> bytes:
        """Converts the packet into stream of bytes. This data must be placed before
        the data being sent by the packet itself."""
        return struct.pack("B", self.version())

    @abc.abstractmethod
    def contents(self) -> Any:
        """Get the contents from data."""
        raise NotImplementedError

    def __repr__(self):
        return f"<Packet-v{self.version()}>"

    @classmethod
    @abc.abstractmethod
    def unique_key(cls) -> Any:
        """A unique value identifying this packet handler."""
        raise NotImplementedError


class PacketRegistery():
    """
    Manages packet version handlers and version implementation handlers. Allowed
    versions range from 1 to 255. Use the class directly instead creating instance.
    """

    packets: ClassVar[Dict[int, Type[Packet]]] = {}
    """stores the packet versions"""

    handlers: ClassVar[Dict[int, Dict[Any, Type[Packet]]]] = {}
    """stores the packet version handlers"""

    @staticmethod
    def register_packet(packet: Type[Packet]) -> Type[Packet]:
        """Register a packet version handler. The packet must define `version`
        staticmethod and should not be duplicate."""
        version = packet.version()
        if version in PacketRegistery.packets.keys():
            logger.warning(
                f"packet-v{version} already registered, registration skipped")
        else:
            PacketRegistery.packets[version] = packet
            logger.info(f"registered packet: {packet!r}")
            PacketRegistery.handlers[version] = {}
        return packet

    @staticmethod
    def register_handler(handler: Type[Packet]) -> Type[Packet]:
        """Register a handler implementing specific version subtype handler. Make sure
        that packet parent must be registered before child is registered."""
        version = handler.version()
        if version not in PacketRegistery.packets.keys():
            logger.warning(f"registering handler for packet-v{version} before parent")
            PacketRegistery.handlers[version] = {}
        key = handler.unique_key()
        PacketRegistery.handlers[version][key] = handler
        logger.info(f"registered handler: {handler!r}")
        return handler

    @staticmethod
    def ensure_regisered() -> List[ModuleType]:
        """Dynamically imports all packet versions packages to make sure they are
        registered."""
        packet_dir = pathlib.Path(__file__).parent
        imported_modules = []
        for subdir in packet_dir.iterdir():
            if subdir.is_dir() and re.fullmatch("^v[0-9]+$", subdir.name):
                module_name = f"{__name__}.{subdir.name}"
                module = importlib.import_module(module_name)
                logger.debug(f"imported module: {module_name}")
                imported_modules.append(module)
        return imported_modules
