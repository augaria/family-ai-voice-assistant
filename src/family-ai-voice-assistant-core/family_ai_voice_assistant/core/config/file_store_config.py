from dataclasses import dataclass

from .config import Config


@dataclass
class FileStoreConfig(Config):
    destination: str = None
