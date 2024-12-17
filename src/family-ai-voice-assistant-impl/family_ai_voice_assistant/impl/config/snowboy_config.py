from dataclasses import dataclass

from family_ai_voice_assistant.core.config import Config


@dataclass
class SnowboyConfig(Config):
    model_path: str = None
