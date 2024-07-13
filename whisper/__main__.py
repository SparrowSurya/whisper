import sys

from whisper.parser import parser
from whisper.core.logger import stream_handler

argv = sys.argv[1:]
obj = parser.parse_args(argv)

if obj.command == "client":
    from .client_app import ClientApp

    stream_handler.setLevel(obj.log)
    client = ClientApp(
        host=obj.host,
        port=obj.port,
        username=obj.user,
    )
    client.run()

if obj.command == "server":
    from .server import Server

    stream_handler.setLevel(obj.log)
    server = Server(
        host=obj.host,
        port=obj.port,
    )
    server.start()