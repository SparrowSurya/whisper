from .conn_reader import ConnReader
from .packet import Packet


class ConnWriter(ConnReader):
    """Writes the data on the stream."""

    def _create_request(self, request: str, enc: str = "utf-8", **kwargs):
        """Create a request."""
        return Packet("request", enc, request=request, **kwargs)

    def create_message(self, text: str, enc: str):
        """Message request."""
        return Packet("message", enc, text=text)

    async def send_message(self, text: str, enc: str = "utf-8"):
        """Send the message over the stream."""
        packet = self._create_message(text, enc)
        await self.write(packet.serialize())

    def exit_request(self, error: Exception, **kwargs):
        """Request to close the connection."""
        return self._create_request("exit", error=error, **kwargs)

    def set_name_request(self, name: str):
        """Request to change the username."""
        return self._create_request("set-name", name=name)
