"""
It provides command line interaction for client.
"""

import sys
import logging

from whisper.settings import APP_NAME, LOG_DIR
from whisper.ui.theme import Palette, Theme
from whisper.logger import Logger, stdout_handler, file_handler
from whisper.packet import PacketRegistery
from .app import App
from .tcp import TcpClient
from .cli import get_parser
from .settings import Setting, Config


program = f"{APP_NAME}.client"
parser = get_parser(program, "whisper.client application")
args = parser.parse_args(sys.argv[1:])

logfile = LOG_DIR / "client.log"
log_handlers = [stdout_handler(), file_handler(str(logfile))]
logger = Logger(program, logging.DEBUG, log_handlers)
logger.debug(f"{program}: {args}")

config = Config(
    host=args.host,
    port=args.port,
)

# TODO: maybe not here
theme = Theme(
    name="Catppuccin-Mocha",
    palette=Palette(
        rosewater="#F5E0DC",
        flamingo="#F2CDCD",
        pink="#F5C2E7",
        mauve="#CBA6F7",
        red="#F38BA8",
        maroon="#EBA0AC",
        peach="#FAB387",
        yellow="#F9E2AF",
        green="#A6E3A1",
        teal="#94E2D5",
        sky="#89DCEB",
        sapphire="#74C7EC",
        blue="#89B4FA",
        lavender="#B4BEFE",
        text="#CDD6F4",
        subtext1="#BAC2DE",
        subtext0="#A6ADC8",
        overlay2="#9399B2",
        overlay1="#7F849C",
        overlay0="#6C7086",
        surface2="#585B70",
        surface1="#45475A",
        surface0="#313244",
        base="#1E1E2E",
        mantle="#181825",
        crust="#11111B",
        danger="#FE8BA8",
        warn="#FAB387",
        success="#A6E3A1",
        info="#89DCEB",
        accent="#CBA8F7",
    ),
    font={
        "family": "Roboto",
        "size": 11,
        "weight": "normal",
    },
)

setting = Setting(config, theme)
setting.data["username"] = args.user

try:
    for module in PacketRegistery.ensure_regisered():
        logger.debug(f"dynamically imported {module.__name__}")
except Exception as ex:
    logger.exception(f"error occured while ensuring packet registeration: {ex}")
else:
    app = App(APP_NAME, logger=logger, setting=setting, conn=TcpClient())
    app.mainloop()
