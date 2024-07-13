import socket
import asyncio
from typing import Tuple


# TODO
# reconnect
# read/write fails
# using ssl
class ClientConnection:
    """
    The class provides the connection management for client. It provides
    asynchronous methods for reading and writing to socket object.

    The class makes use of `asyncio` event loop for asynchronous tasks.
    """

    __slots__ = ("sock", "__connected")

    def __init__(self):
        """
        Initialises the underlying TCP socket for the client. The socket
        is set to non-blocking.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__connected = False

    def address(self) -> Tuple[str, int]:
        """Client address as tuple of hostname and port address.

        NOTE - Must make sure that connection is established.

        Raises:
        * OSError - if client is not connected (some platforms).
        """
        return self.sock.getsockname()

    @property
    def is_connected(self) -> bool:
        """Check is client is connected."""
        # This doen not ensure that underlying connection is still alive
        # and can send or receive data
        return self.__connected

    def connect(self, host: str, port: int):
        """Connect to server.

        Arguments:
        * host - server hostname/ip address.
        * port - server port address.

        Raises:
        * RuntimeError - if client is already connected.
        * ConnectionRefusedError - if unable to connect.
        """
        if self.is_connected:
            raise RuntimeError("Connection already established")

        # connect needs to be waited to complete the operation otherwise
        # BlockingIOError: [Errno 115] Operation now in progress
        self.sock.setblocking(True)
        self.sock.connect((host, port))
        self.sock.setblocking(False)
        self.__connected = True

    def disconnect(self):
        """Close the connection.

        Raises:
        * RuntimeError - client is not connected.
        """
        if not self.is_connected:
            raise RuntimeError("Connection already established")

        self.sock.close()
        self.__connected = False

    async def read(self, n: int, loop: asyncio.AbstractEventLoop):
        """Read n bytes of data from connection."""
        return await loop.sock_recv(self.sock, n)

    async def write(self, data: bytes, loop: asyncio.AbstractEventLoop):
        """Write data to the connection."""
        return await loop.sock_sendall(self.sock, data)
