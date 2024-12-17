from dataclasses import dataclass
from typing import List

from family_ai_voice_assistant.core.config import Config
from family_ai_voice_assistant.core.contracts import Language


language_map = {
    Language.EN: "en-US",
    Language.CHS: "zh-CN",
}


@dataclass
class AzureSpeechVoice:
    name: str
    language: str


@dataclass
class AzureSpeechConfig(Config):
    api_region: str = None
    api_key: str = None
    voice: List[AzureSpeechVoice] = None
