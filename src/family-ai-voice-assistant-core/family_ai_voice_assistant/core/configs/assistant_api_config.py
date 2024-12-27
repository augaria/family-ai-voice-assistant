from dataclasses import dataclass
from .config import Config


@dataclass
class AssistantApiConfig(Config):
    port: int = None
