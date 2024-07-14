import sys

from whisper.parser import parser, log_levels
from whisper.core.logger import stream_handler

argv = sys.argv[1:]
obj = parser.parse_args(argv)
stream_handler.setLevel(log_levels[obj.log])


if obj.command == "client":
    from .client_app import ClientApp

    client = ClientApp(
        host=obj.host,
        port=obj.port,
        username=obj.user,
    )
    client.run()

if obj.command == "server":
    from .server import Server

    server = Server(
        host=obj.host,
        port=obj.port,
    )
    server.run()
