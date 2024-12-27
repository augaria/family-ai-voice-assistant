from dataclasses import dataclass

from family_ai_voice_assistant.core.configs import Config
from family_ai_voice_assistant.core.contracts import Language

coqui_tts_language_map = {
    Language.EN: "en",
    Language.CHS: "zh-cn",
}


@dataclass
class CoquiTTSConfig(Config):
    model: str = None
    speaker_id: str = None
    speaker_wav: str = None
