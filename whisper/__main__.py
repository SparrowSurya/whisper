import sys
import asyncio

from whisper.parser import parser


argv = sys.argv[1:]
obj = parser.parse_args(argv)

if obj.command == "client":
    from .client import ClientApp

    client = ClientApp(
        host=obj.host,
        port=obj.port,
        username=obj.user,
    )
    client.run()

elif obj.command == "server":
    from .server import Server

    server = Server(
        host=obj.host,
        port=obj.port,
    )
    asyncio.run(server.run())