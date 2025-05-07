"""
This module provides base client object providing communication support with server
using packet. It also provide limited support of connection management.
"""

import logging
from enum import StrEnum, auto

from whisper.common import Address
from whisper.packet import Packet
from whisper.typing import (
    TcpClient as _TcpClient,
    EventLoop as _EventLoop
)


logger = logging.getLogger(__name__)

class ConnState(StrEnum):
    """Connection state."""

    NOT_CONNECTED = auto()
    CONNECTED = auto()


class BaseClient:
    """
    Base Client class providing asynchronous communication with server via packets. It
    also manages connection state (to some extent for now).
    """

    def __init__(self, conn: _TcpClient):
        """Requires a connection object to connect to server."""
        self.conn = conn
        self.conn_state = ConnState.NOT_CONNECTED

    @property
    def is_connected(self) -> bool:
        """
        This does not ensure that data can be sent or received over the
        connection.
        """
        return self.conn_state is ConnState.CONNECTED

    def server_address(self) -> Address:
        """Provides the connected server address."""
        return self.conn.sock.getpeername()

    def open_connection(self, host: str, port: int):
        """Connect to server with given address."""
        self.conn.open(host, port)
        self.conn_state = ConnState.CONNECTED
        logger.info(f"connection established with {host}:{port}")

    def close_connection(self):
        """Closes connection."""
        self.conn.close()
        self.conn_state = ConnState.NOT_CONNECTED
        logger.info("connection closed")

    async def read(self, loop: _EventLoop) -> Packet:
        """Read packet from server."""
        reader = lambda n: self.conn.read(n, loop)  # noqa: E731
        packet = await Packet.from_stream(reader)
        logger.debug(f"received packet: {packet!r}")
        return packet

    async def write(self, packet: Packet, loop: _EventLoop):
        """Write packet to server."""
        data = packet.to_stream()
        await self.conn.write(data, loop)
        logger.debug(f"sent packet: {packet!r}")
