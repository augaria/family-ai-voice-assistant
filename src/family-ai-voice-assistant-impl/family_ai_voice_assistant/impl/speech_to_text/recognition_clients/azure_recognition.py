from typing import Any, Union

from speech_recognition import Recognizer, exceptions, AudioData

from family_ai_voice_assistant.core.clients import RecognitionClient
from family_ai_voice_assistant.core.telemetry import trace
from family_ai_voice_assistant.core.configs import (
    ConfigManager,
    SpeechRecognitionConfig
)
from family_ai_voice_assistant.core.helpers.language_manager import (
    LanguageManager
)
from family_ai_voice_assistant.core.logging import Loggers

from ...configs import AzureSpeechConfig, azure_speech_language_map


class AzureRecognition(RecognitionClient):

    def __init__(self):

        speech_recognition_config = ConfigManager().get_instance(
            SpeechRecognitionConfig
        )
        if speech_recognition_config is None:
            raise ValueError("SpeechRecognitionConfig is not set.")

        self._agent = Recognizer()
        self._agent.pause_threshold = (
            speech_recognition_config.pause_threshold
        )
        self._agent.energy_threshold = (
            speech_recognition_config.energy_threshold
        )

        self._azure_speech_config = ConfigManager().get_instance(
            AzureSpeechConfig
        )
        if self._azure_speech_config is None:
            raise ValueError("AzureSpeechConfig is not set.")

    @trace()
    def recognize(self, audio: Union[AudioData, Any]) -> str:
        try:
            if not isinstance(audio, AudioData):
                raise ValueError(
                    "AudioData format is required for AzureRecognition"
                )
            voice_language = azure_speech_language_map[LanguageManager().get()]
            res = self._agent.recognize_azure(
                audio,
                key=self._azure_speech_config.api_key,
                language=voice_language,
                location=self._azure_speech_config.api_region
            )
        except exceptions.UnknownValueError:
            Loggers().recognition.warning(
                "Azure Speech Recognition could not understand audio"
            )
        except exceptions.RequestError as e:
            Loggers().recognition.warning(
                f"Could not request results from Azure Speech service: {e}")

        return res[0]
