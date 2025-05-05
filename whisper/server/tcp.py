"""
This module provides connection class for server.
"""

import socket
from typing import Tuple

from whisper.common import Address
from whisper.typing import (
    EventLoop as _EventLoop,
)


class TcpServer:
    """
    A TCP oriented asynchronous server connection. It uses `asyncio` event loop to
    performs accept, read and write operations on socket.
    """

    def __init__(self):
        """Initialises the underlying TCP socket."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def address(self) -> Address:
        """Server host address as tuple of hostname and port address. Make sure that
        server is serving before it is called."""
        return self.sock.getsockname()

    def start(self, host: str, port: int):
        """Start the server and listen for incoming connection."""
        self.sock.bind((host, port))
        self.sock.listen(0)

    def stop(self):
        """Stop the server."""
        self.sock.close()

    async def accept(self, loop: _EventLoop) -> Tuple[socket.socket, Address]:
        """Accepts incoming connection."""
        return await loop.sock_accept(self.sock)  # type: ignore

    async def read(self, sock: socket.socket, n: int, loop: _EventLoop) -> bytes:
        """Reads `n` bytes from socket."""
        return await loop.sock_recv(sock, n)  # type: ignore

    async def write(self, sock: socket.socket, data: bytes, loop: _EventLoop):
        """Write `data` to the socket."""
        return await loop.sock_sendall(sock, data) # type: ignore
