"""
It provides command line interaction for client.
"""

import sys
import argparse
import logging

from whisper.settings import APP_NAME
from whisper.cli import HostAction, PortAction
from whisper.logger import Logger, stdout_handler, file_handler
from .app import App
from .settings import ClientSetting


PROGRAM = f"{APP_NAME}.client"

parser = argparse.ArgumentParser(
    PROGRAM,
    description="run client app",
)

parser.add_argument(
    "-ip", "--host",
    metavar="HOST",
    type=str,
    action=HostAction,
    required=False,
    default="localhost",
    help="server host address",
)

parser.add_argument(
    "-p", "--port",
    metavar="PORT",
    type=int,
    action=PortAction,
    required=False,
    default=12345,
    help="server port number",
)

parser.add_argument(
    "-u", "--user",
    metavar="USER",
    type=str,
    required=False,
    default="",
    help="user name",
)

# TODO: use ENV setting for devleopment based customization
log_handlers = [stdout_handler, file_handler]
logger = Logger(APP_NAME, logging.DEBUG, log_handlers)

args = parser.parse_args(sys.argv[1:])

setting = ClientSetting.defaults(
    host=args.host,
    port=args.port,
)
setting.data["username"] = args.user

app = App(APP_NAME, logger=logger, setting=setting)
app.mainloop()
