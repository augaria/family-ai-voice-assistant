from dataclasses import dataclass

from .config import Config
from ..contracts import Language


@dataclass
class GeneralConfig(Config):
    language: Language = Language.CHS
    timezone: str = 'Asia/Shanghai'
    bot_name: str = None
    greeting_words_path: str = None
