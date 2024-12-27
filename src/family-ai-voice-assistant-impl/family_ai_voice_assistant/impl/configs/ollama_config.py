from dataclasses import dataclass

from family_ai_voice_assistant.core.configs import Config


@dataclass
class OllamaConfig(Config):
    host: str = None
    model: str = None
