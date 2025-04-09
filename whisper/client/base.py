"""
This module provides base client object providing communication support with server
using packet. It also provide limited support of connection management.
"""

import asyncio
from enum import StrEnum, auto
from typing import Tuple

from whisper.packet import Packet
from .tcp import TcpClient


class ConnState(StrEnum):
    """Connection state."""

    NOT_CONNECTED = auto()
    """No Connection is established."""

    CONNECTED = auto()
    """Connection is established."""


class BaseClient:
    """
    Base Client class providing asynchronous communication with server via packets. It
    also manages connection state (to some extent for now).
    """

    def __init__(self, conn: TcpClient | None = None):
        """Requires a connection object to connect to server."""
        self.conn = conn or TcpClient()
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
        return self.conn.sock.getpeername()

    def open_connection(self, host: str, port: int):
        """Connect to server with given address."""
        self.conn.open(host, port)
        self.conn_state = ConnState.CONNECTED

    def close_connection(self):
        """Closes connection."""
        self.conn.close()
        self.conn_state = ConnState.NOT_CONNECTED

    async def read(self, loop: asyncio.AbstractEventLoop) -> Packet:
        """Read packet from server."""
        reader = lambda n: self.conn.read(n, loop)  # noqa: E731
        return await Packet.from_stream(reader)

    async def write(self, packet: Packet, loop: asyncio.AbstractEventLoop):
        """Write packet to server."""
        data = packet.to_stream()
        return await self.conn.write(data, loop)
