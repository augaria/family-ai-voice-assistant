from dataclasses import dataclass
from typing import List

from family_ai_voice_assistant.core.configs import Config


@dataclass
class PicovoiceConfig(Config):
    api_key: str = None
    model_path: str = None
    keyword_paths: List[str] = None
