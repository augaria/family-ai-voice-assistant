from dataclasses import dataclass

from .config import Config
from ..contracts import Language


@dataclass
class GeneralConfig(Config):
    language: Language = Language.CHS
    timezone: str = None
    bot_name: str = None
    user_name: str = None
    city: str = None
    greeting_words_path: str = None
