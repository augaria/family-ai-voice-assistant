from dataclasses import dataclass

from .config import Config


@dataclass
class HistoryStoreConfig(Config):
    connection_str: str = None
    database_name: str = None
    collection_name: str = None
