"""
This module provides connection object for client.
"""

import socket
import asyncio
from typing import Tuple


class ClientConn:
    """
    A TCP oriented asynchronous client connection. It uses `asyncio`
    event loop to performs read and write operations on socket.
    """

    def __init__(self):
        """Initialize TCP socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def address(self) -> Tuple[str, int]:
        """
        Provides client address as tuple of hostname and port address.
        Make sure that client is connected before calling it.
        """
        return self.sock.getsockname()

    def open(self, host: str, port: int):
        """Establish connection with server."""
        # connect needs to be waited to complete the operation otherwise
        # BlockingIOError: [Errno 115] Operation now in progress
        self.sock.setblocking(True)
        self.sock.connect((host, port))
        self.sock.setblocking(False)

    def close(self):
        """Close the connection with server."""
        self.sock.close()

    async def read(self,
        n: int,
        loop: asyncio.AbstractEventLoop,
    ) -> bytes:
        """Read `n` bytes of data from server."""
        return await loop.sock_recv(self.sock, n)

    async def write(self,
        data: bytes,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        """Write data to the server."""
        return await loop.sock_sendall(self.sock, data)
