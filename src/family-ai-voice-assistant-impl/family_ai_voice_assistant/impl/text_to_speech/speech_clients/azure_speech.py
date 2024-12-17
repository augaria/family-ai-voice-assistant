from typing import Dict

from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer
)
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from family_ai_voice_assistant.core.clients import SpeechClient
from family_ai_voice_assistant.core.config import ConfigManager
from family_ai_voice_assistant.core.contracts import Language
from family_ai_voice_assistant.core.utils.language_manager import (
    LanguageManager
)

from ..waitable_result_clients.azure_speech_result import AzureSpeechResult
from ...config import AzureSpeechConfig, language_map


class AzureSpeech(SpeechClient):

    def __init__(self):
        config = ConfigManager().get_instance(AzureSpeechConfig)
        self._synthesizers: Dict[Language, SpeechSynthesizer] = {}

        if config is None:
            raise ValueError("AzureSpeechConfig is not set.")
        for language in Language:
            self._add_synthesizer(language, config)

    def _add_synthesizer(
        self,
        language: Language,
        config: AzureSpeechConfig
    ):
        speech_config = SpeechConfig(
            subscription=config.api_key,
            region=config.api_region
        )
        for voice in config.voice:
            if voice.language == language_map[language]:
                speech_config.speech_synthesis_voice_name = voice.name
                break

        audio_config = AudioOutputConfig(use_default_speaker=True)

        self._synthesizers[language] = SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

    def speech_async(self, text: str) -> AzureSpeechResult:
        result_future = (
            self._synthesizers[LanguageManager().get()].speak_text_async(text)
        )
        return AzureSpeechResult(result_future)

    def stop_async(self) -> AzureSpeechResult:
        result_future = (
            self._synthesizers[LanguageManager().get()].stop_speaking_async()
        )
        return AzureSpeechResult(result_future)
