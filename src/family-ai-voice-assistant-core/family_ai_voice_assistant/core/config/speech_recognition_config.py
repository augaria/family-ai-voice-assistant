from dataclasses import dataclass

from family_ai_voice_assistant.core.config import Config


@dataclass
class SpeechRecognitionConfig(Config):
    timeout: int = None
    phrase_time_limit: int = None
    energy_threshold: int = 300
    pause_threshold: int = 3
