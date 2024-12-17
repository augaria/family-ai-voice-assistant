from dataclasses import dataclass

from family_ai_voice_assistant.core.config import Config


@dataclass
class OpenAIConfig(Config):
    api_key: str = None
    model: str = None
    max_token_per_session: int = -1
