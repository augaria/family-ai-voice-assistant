from dataclasses import dataclass

from family_ai_voice_assistant.core.configs import Config
from family_ai_voice_assistant.core.contracts import Language

openai_whisper_language_map = {
    Language.EN: "en",
    Language.CHS: "zh",
}


@dataclass
class OpenAIWhisperConfig(Config):
    model: str = None
