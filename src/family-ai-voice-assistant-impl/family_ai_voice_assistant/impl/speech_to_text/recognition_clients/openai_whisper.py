from typing import Any, Union

import whisper
import torch
from speech_recognition import AudioData

from family_ai_voice_assistant.core.clients import RecognitionClient
from family_ai_voice_assistant.core.telemetry import trace
from family_ai_voice_assistant.core.configs import (
    ConfigManager
)
from family_ai_voice_assistant.core.helpers.language_manager import (
    LanguageManager
)
from family_ai_voice_assistant.core.logging import Loggers
from family_ai_voice_assistant.core.utils.wav_utils import WavUtils

from ...configs import OpenAIWhisperConfig, openai_whisper_language_map


class OpenAIWhisper(RecognitionClient):

    def __init__(self):
        openai_whisper_config = ConfigManager().get_instance(
            OpenAIWhisperConfig
        )
        if openai_whisper_config is None:
            raise ValueError("OpenAIWhisperConfig is not set.")
        if (
            openai_whisper_config.model is None
            or openai_whisper_config.model == ""
        ):
            raise ValueError("OpenAIWhisperConfig.model is not set.")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._client = whisper.load_model(
            openai_whisper_config.model,
            device=device
        )

    @trace()
    def recognize(self, audio: Union[AudioData, Any]) -> str:
        try:
            if not isinstance(audio, AudioData):
                raise ValueError(
                    "AudioData format is required for OpenaiWhisperRecognition"
                )

            audio_file = WavUtils.write_wav_file_from_bytes(
                audio.get_wav_data()
            )
            language = openai_whisper_language_map[LanguageManager().get()]
            res = self._client.transcribe(audio_file, language=language)
            return res['text']
        except Exception as e:
            Loggers().recognition.warning(
                f"Could not request results from Openai Whisper sdk: {e}"
            )
            return ""
