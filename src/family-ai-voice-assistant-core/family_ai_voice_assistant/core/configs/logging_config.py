from dataclasses import dataclass
import logging


from .config import Config


@dataclass
class LoggingConfig(Config):
    path: str = None
    level: str = logging.INFO
