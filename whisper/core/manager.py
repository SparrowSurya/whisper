import json
from typing import Dict, Any

from whisper.components.chat import Chat
from whisper.core.chat import Handle


class Manager:
    """Manages chats and handles."""

    handle: Handle

    def __init__(self, app):
        self.app = app

    def create_handle(self, chat: Chat) -> Handle:
        """Creates a new chat handle."""
        self.handle = Handle(self.send, chat.recv)
        return self.handle

    def dispatch(self, data: bytes):
        """Show the message in the chat."""
        content = self.deserialize(data)
        self.handle.recv(content)

    def send(self, content: Dict[str, Any]):
        """Callback made by the chat ui to send message out to server."""
        data = self.serialize(content)
        self.app.create_task(self.app.conn.write(data))

    def serialize(self, content: Dict[str, Any]) -> bytes:
        """Json object serializer."""
        return bytes(
            json.dumps(content, ensure_ascii=False, sort_keys=False), encoding="utf-8"
        )

    def deserialize(self, data: bytes) -> Dict[str, Any]:
        """Json data deserializer."""
        return json.loads(data.decode(encoding="utf-8"))
