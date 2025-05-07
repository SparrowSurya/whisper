"""
It provides command line interface for server.
"""

import sys
import logging

from whisper.settings import APP_NAME, LOG_DIR
from whisper.logger import setup_logging, cleanup_logging
from whisper.packet import PacketRegistery
from .backend import Server
from .tcp import TcpServer
from .cli import get_parser


program = f"{APP_NAME}.server"
parser = get_parser(program, "whisper.server cli application")
args = parser.parse_args(sys.argv[1:])

logfile = LOG_DIR / "server.log"
setup_logging(level=logging.DEBUG, logfile=logfile)

logger = logging.getLogger(__name__)
logger.debug(f"{program} invoked: {args}")

PacketRegistery.ensure_regisered()
server = Server(conn=TcpServer())

try:
    server.run(host=args.host, port=args.port)
except Exception as ex:
    logger.exception(f"uncaught exception in {program}: {ex}")
else:
    cleanup_logging()
