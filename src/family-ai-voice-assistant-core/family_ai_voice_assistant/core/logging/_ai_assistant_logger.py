import logging
import copy
import os
from colorama import init, Fore, Style
from logging.handlers import TimedRotatingFileHandler

from ..configs import ConfigManager, LoggingConfig

init(autoreset=True)


logging_format_template = (
    '%(asctime)-20s %(name)-20s %(levelname)-18s %(message)s'
)


def colored_print(text: str, fore_color: str, end='\r\n'):
    print(fore_color + text + Style.RESET_ALL, end=end)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED,
    }

    def format(self, record):
        record = copy.copy(record)
        levelname = record.levelname
        if levelname in self.COLORS:
            color = self.COLORS[levelname]
            record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"

        formatted_message = super().format(record)

        return f"{color}{formatted_message}{Style.RESET_ALL}"


class AIAssistantLogger(logging.Logger):

    def __init__(self, name):
        super().__init__(f"[{name}]")

        config = ConfigManager().get_instance(LoggingConfig)

        if config and config.level:
            self.setLevel(config.level)
        else:
            self.setLevel(logging.INFO)

        self._add_stream_handler()

        if config and config.path:
            self._add_file_handler(path=config.path)

    def _add_stream_handler(self):
        console_formatter = ColoredFormatter(logging_format_template)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.addHandler(console_handler)

    def _add_file_handler(self, path: str):

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        file_handler = TimedRotatingFileHandler(
            filename=path,
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        file_formatter = logging.Formatter(logging_format_template)
        file_handler.setFormatter(file_formatter)
        self.addHandler(file_handler)
