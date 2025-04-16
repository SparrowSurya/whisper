"""
This module provides tcp connection object for client.
"""

import socket

from whisper.typing import (
    Address as _Address,
    EventLoop as _EventLoop,
)


class TcpClient:
    """
    A TCP oriented asynchronous client connection. It uses `asyncio` event loop to
    perform read and write operations on socket. It abstracts all the lower level
    non blocking socket io implementations.
    """

    def __init__(self):
        """Initialize TCP non-blocking socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def address(self) -> _Address:
        """
        Provides client address as tuple of hostname and port address. Make sure that
        client is connected before calling it.
        """
        return self.sock.getsockname()

    def open(self, host: str, port: int):
        """Establish socket connection with given address."""
        # connect needs to be waited to complete the operation otherwise
        # BlockingIOError: [Errno 115] Operation now in progress
        self.sock.setblocking(True)
        self.sock.connect((host, port))
        self.sock.setblocking(False)

    def close(self):
        """Closes the socket connection."""
        self.sock.close()

    async def read(self, n: int, loop: _EventLoop) -> bytes:
        """Read `n` bytes of data from socket."""
        return await loop.sock_recv(self.sock, n)

    async def write(self, data: bytes, loop: _EventLoop) -> None:
        """Write data to the socket."""
        return await loop.sock_sendall(self.sock, data)
