"""
It provides command line interface for server.
"""

import sys
import logging

from whisper.settings import APP_NAME, LOG_DIR
from whisper.logger import Logger, stdout_handler, file_handler
from .backend import Server
from .tcp import TcpServer
from .cli import get_parser


program = f"{APP_NAME}.server"
parser = get_parser(program, "whisper.server cli application")
args = parser.parse_args(sys.argv[1:])

logfile = LOG_DIR / "server.log"
log_handlers = [stdout_handler(), file_handler(logfile)]
logger = Logger(APP_NAME, logging.DEBUG, log_handlers) # type: ignore
logger.debug(f"{program}: {args}")

server = Server(logger=logger, conn=TcpServer())
server.run(host=args.host, port=args.port)
