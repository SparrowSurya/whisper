"""
This module provides basic client functionality for communication with
server with connection management (to some extent).
"""

import asyncio
from enum import StrEnum, auto
from typing import Tuple

from whisper.core.packet import Packet
from .connection import ClientConn


class ConnState(StrEnum):
    """Connection state."""

    NOT_CONNECTED = auto()
    """No Connection is established."""

    CONNECTED = auto()
    """Connection is established."""


class BaseClient:
    """
    Base Client class provides a mechanism (packet) to communicate with
    server. It also manages the connection state. It allows to read and
    write packets to and from server.
    """

    def __init__(self, conn: ClientConn | None = None):
        """Requires a connection object to connect to server."""
        self.connection = conn or ClientConn()
        self.conn_state = ConnState.NOT_CONNECTED

    @property
    def is_connected(self) -> bool:
        """
        This does not ensure that data can be sent or received over the
        connection.
        """
        return self.conn_state is ConnState.CONNECTED

    def server_address(self) -> Tuple[str, int]:
        """Provides the connected server address."""
        return self.connection.sock.getpeername()

    def open_connection(self, host: str, port: int):
        """Connect to server with given address."""
        self.connection.open(host, port)
        self.conn_state = ConnState.CONNECTED

    def close_connection(self):
        """Closes connection."""
        self.connection.close()
        self.conn_state = ConnState.NOT_CONNECTED

    async def read(self, loop: asyncio.AbstractEventLoop) -> Packet:
        """Read packet from server."""
        reader = lambda n: self.connection.read(n, loop)  # noqa: E731
        return await Packet.from_stream(reader)

    async def write(self,
        packet: Packet,
        loop: asyncio.AbstractEventLoop,
    ):
        """Write packet to server."""
        data = packet.to_stream()
        return await self.connection.write(data, loop)
