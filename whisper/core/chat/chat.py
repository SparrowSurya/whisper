from typing import Dict, Any


class BaseChat:
    """Base chat class."""

    def __init__(self, app):
        """App refers to the main application."""
        self.app = app
        self.handle = self.app.manager.create_handle(self)

    def send(self, content: Dict[str, Any]):
        """Message sent in the chat."""
        self.handle.send(content)

    def recv(self, content: Dict[str, Any]):
        """This is required to be implemented by the child class."""
        cls_name = self.__class__.__name__
        msg = f"This method should be defined in the child class of the {cls_name}."
        raise NotImplementedError(msg)

    def create_content(self, text: str) -> Dict[str, Any]:
        """Creats an object to store message."""
        return {
            "type": "message",
            "text": text,
        }
