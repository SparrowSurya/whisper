import socket
import asyncio
from typing import Any, Coroutine, Tuple


class ServerConnection:
    """
    The class provides connection management for the server. It provides
    asynchronous functions for listening incoming connections, reading
    incoming data and writing outgoing data.

    The class makse use of `asyncio` event loop for asynchronous tasks.
    """

    __slots__ = ("sock", "__serving")

    def __init__(self):
        """
        Initialises the underlying TCP socket for the server. The socket
        is set to non-blocking.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__serving = False

    @property
    def address(self) -> Tuple[str, int]:
        """Server host address as tuple of hostname and port address.

        NOTE - Make sure that server is serving.

        Raises:
        * OSError - if server is not bind to an address (some platforms).
        """
        return self.sock.getsockname()

    @property
    def is_serving(self) -> bool:
        """Check If server has started."""
        return self.__serving

    def start(self, host: str, port: int):
        """
        Opens the connection and listen for incoming connection.

        Arguments:
        * host - server hostname.
        * port - server port address.

        Raises:
        * RuntimeError - server is already serving.
        * OSError - address is already in use.
        """
        if self.is_serving:
            raise RuntimeError("Server already running")

        self.sock.bind((host, port))
        self.sock.listen(0)
        self.__serving = True

    def stop(self):
        """
        Close the server.

        Raises:
        * RuntimeError - if server is not serving.
        """
        if not self.is_serving:
            raise RuntimeError("Server is not running")

        self.sock.close()
        self.__serving = False

    async def accept(
        self,
        loop: asyncio.AbstractEventLoop,
    ) -> Coroutine[Any, Any, Tuple[socket.socket, Tuple[str, int]]]:
        """
        Accept incoming connection.

        Returns:
        * connection socket.
        * tuple of connection address as hostname and port address.
        """
        return await loop.sock_accept(self.sock)  # type: ignore

    async def read(
        self,
        sock: socket.socket,
        n: int,
        loop: asyncio.AbstractEventLoop,
    ):
        """Reads n bytes from socket."""
        return await loop.sock_recv(sock, n)

    async def write(
        self,
        sock: socket.socket,
        data: bytes,
        loop: asyncio.AbstractEventLoop,
    ):
        """Write data to the socket."""
        return await loop.sock_sendall(sock, data)
