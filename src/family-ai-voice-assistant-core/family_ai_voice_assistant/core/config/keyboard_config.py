from dataclasses import dataclass

from .config import Config


@dataclass
class KeyboardConfig(Config):
    device: str = None
