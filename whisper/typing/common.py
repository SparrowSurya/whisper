"""
This module provides common type annotations for other typing modules.
"""

from socket import socket
from typing import Tuple, Generic, TypeVar, Protocol


Address = Tuple[str, int]

class EventLoop(Protocol):
    async def sock_accept(self, sock: socket) -> Tuple[socket, Address]: ...
    async def sock_recv(self, sock: socket, n: int) -> bytes: ...
    async def sock_sendall(self, sock: socket, data: bytes): ...

P = TypeVar("P")

class AsyncQueue(Generic[P]):
    async def put(self, item: P): ...
    async def get(self) -> P: ...
