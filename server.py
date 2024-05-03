import json
import asyncio
from dataclasses import dataclass
from typing import Dict, Tuple, List, Any, Optional


@dataclass
class Connection:
    """Dataclass holding info about the connection."""

    addr: Tuple[str, int]
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    username: Optional[str] = None
    run_forever: bool = True

    @property
    def name(self) -> str:
        """provides username is exists otherwise address."""
        return self.username if self.username else str(self.addr)


class AsyncServer:
    """Asynchronous chat server.

    Manages the different clients connected with the server.
    Currently server does not suport chat room and currenly puts all clients
    in single global chat per server.

    It currently supports only JSON serializable requests with following scheme:
    * type - type of content (message | action)
        1. message - the request must contain `message`.
        2. action - name of the action.
            * set-name: sets the name of the client.
                * requied field - name
                * NOTE - client cannot send message until name is not provided.
            * exit: informs the chat that a client has left.

    Output response (JSON):
    * message - message to display.
    * user - owner of message if None then sent by server.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._conns: List[Connection] = []

    def register(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> Connection:
        """Register the streams for a connection."""
        addr = writer.get_extra_info("peername")
        conn = Connection(addr, reader, writer, None)
        self._conns.append(conn)
        print(f"Connected with {addr}")
        return conn

    def unregister(self, conn: Connection):
        """Unregister the connection."""
        self._conns.remove(conn)
        print(f"Removed {conn.addr} with username {conn.username}")

    def serialize(self, req: Dict[str, Any]) -> bytes:
        """Serializes the request."""
        return bytes(
            json.dumps(req, ensure_ascii=False, sort_keys=False), encoding="utf-8"
        )

    def deserialize(self, data: bytes) -> Dict[str, Any]:
        """Deserializes the data into request."""
        return json.loads(data.decode(encoding="utf-8"))

    async def broadcast(self, data: bytes):
        """Broadcast the data to all clients."""
        for conn in self._conns:
            conn.writer.write(data)
            await conn.writer.drain()

    def process_name(self, conn: Connection, new_name: str) -> Dict[str, Any]:
        """Responds the request to change name."""
        old_name = conn.username
        conn.username = new_name

        if old_name is not None:
            text = f"{old_name} changed to {new_name}!"
            print(text)
        else:
            text = f"{new_name} joined!"
            print(f"{conn.addr} joined as {new_name}")

        return {
            "user": None,
            "text": text,
        }

    def process_exit(self, conn: Connection) -> Dict[str, Any] | None:
        """Responds the request to exit."""
        print(f"{conn.name} exited!")
        conn.run_forever = False
        if conn.username is not None:
            return {
                "user": None,
                "text": f"{conn.username} exited",
            }
        return None

    def process_message(self, conn: Connection, text: str) -> Dict[str, Any] | None:
        """Responds the request to send message."""
        print(f"{conn.name}: {text}")
        name = conn.username
        if name is not None:
            return {"user": conn.username, "text": text}
        return None

    async def respond(self, conn: Connection, data: bytes):
        """Creates an appropriate response from data received from connection."""
        content = self.deserialize(data)
        response = None
        typ = content["type"]

        if typ == "set-name":
            response = self.process_name(conn, content["name"])
        elif typ == "exit":
            response = self.process_exit(conn)
        elif typ == "message":
            response = self.process_message(conn, content["text"])

        if response is not None:
            await self.broadcast(self.serialize(response))

    async def client_handle(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Client handler to listen data from it."""
        conn = self.register(reader, writer)

        async def coro():
            while conn.run_forever:
                data = await reader.read(4096)
                if data:
                    await self.respond(conn, data)

        try:
            await coro()
        except asyncio.CancelledError:
            pass
        except Exception as err:
            print(f"Error {conn.name}:", err)
        finally:
            self.unregister(conn)
            writer.close()
            await writer.wait_closed()

    async def mainloop(self):
        """Start the server."""
        server = await asyncio.start_server(self.client_handle, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"server listening on {addr}")
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    server = AsyncServer("localhost", 3000)
    asyncio.run(server.mainloop())
