"""
This module provide abstract base class for handelling packets.
"""

import abc
from collections.abc import Mapping, Sequence
from typing import Tuple, Any, Generic, TypeVar, Union

from whisper.packet import Packet


_P = TypeVar("_P", bound=Packet)
_A = TypeVar("_A", bound=Any)


class AbstractPacketHandler(abc.ABC, Generic[_P, _A]):
    """Common abstract packet handler class for packet handelling."""

    def __init__(self, app: _A):
        """Provide the application instance."""
        self.app = app

    @abc.abstractmethod
    def validate_packet(self, packet: _P):
        """Validate the packet. Raise error if validation fails. It ensures that this
        handler can handle given packet or not."""
        raise NotImplementedError

    def __call__(self, packet: _P, /, *args) -> Any:
        """Call the handler instance directly with packet instance."""
        self.validate_packet(packet)
        content = packet.contents()

        if (isinstance(content, tuple)
            and len(content) == 2
            and isinstance(content[0], Sequence)
            and not isinstance(content[0], (str, bytes))
            and isinstance(content[1], Mapping)
        ):
            self.handle(*args, *content[0], **content[1])
        elif isinstance(content, Mapping):
            self.handle(*args, **content)
        elif isinstance(content, Sequence) and not isinstance(content, (str, bytes)):
            self.handle(*args, *content)
        else:
            return self.handle(*args, content)

    @abc.abstractmethod
    def handle(self, *args: Any, **kwargs: Any) -> Union[
        Any,
        Sequence[Any],
        Mapping[str, Any],
        Tuple[Sequence, Mapping[str, Any]],
    ]:
        """Perform required actions."""
        raise NotImplementedError
