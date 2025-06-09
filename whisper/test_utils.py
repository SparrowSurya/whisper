import asyncio
from typing import Callable, Awaitable


def stream_reader(data: bytes) -> Callable[[int], Awaitable[bytes]]:
    """Provides async callback to read given data as stream."""

    def read(data: bytes):
        def _read(n: int) -> bytes:
            nonlocal data
            chunk, data = data[:n], data[n:]
            return chunk
        return _read

    async def reader(n: int, reader: Callable[[int], bytes]):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, reader, n)

    _read = read(data)
    return lambda n: reader(n, _read)
