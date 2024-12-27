from dataclasses import dataclass

from family_ai_voice_assistant.core.configs import Config


@dataclass
class AzureOpenAIConfig(Config):
    api_base: str = None
    api_key: str = None
    api_version: str = None
    deployment_name: str = None
    max_token_per_session: int = -1
