"""
This module provides connection object for server.
"""

import socket
import asyncio
import logging
from typing import Tuple


logger = logging.getLogger(__name__)


class ServerConn:
    """
    A TCP oriented asynchronous server connection. It uses `asyncio`
    event loop to performs accept, read and write operations on socket.
    """

    def __init__(self):
        """Initialises the underlying TCP socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__serving = False

    def address(self) -> Tuple[str, int]:
        """
        Server host address as tuple of hostname and port address. Make
        sure that server is serving before it is called.
        """
        return self.sock.getsockname()

    @property
    def is_serving(self) -> bool:
        """Check if server has started."""
        return self.__serving

    def start(self, host: str, port: int):
        """Start the server and listen for incoming connection."""
        if self.is_serving:
            msg = "Server is already running!"
            logger.error(msg)
            raise RuntimeError(msg)

        self.sock.bind((host, port))
        self.sock.listen(0)
        self.__serving = True

    def stop(self):
        """Stop the server."""
        if not self.is_serving:
            msg = "Server is not running!"
            logger.error(msg)
            raise RuntimeError(msg)

        self.sock.close()
        self.__serving = False

    async def accept(
        self,
        loop: asyncio.AbstractEventLoop,
    ) -> Tuple[socket.socket, Tuple[str, int]]:
        """Accepts incoming connection."""
        return await loop.sock_accept(self.sock)  # type: ignore

    async def read(
        self,
        sock: socket.socket,
        n: int,
        loop: asyncio.AbstractEventLoop,
    ) -> bytes:
        """Reads `n` bytes from socket."""
        return await loop.sock_recv(sock, n)  # type: ignore

    async def write(
        self,
        sock: socket.socket,
        data: bytes,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        """Write `data` to the socket."""
        return await loop.sock_sendall(sock, data) # type: ignore
