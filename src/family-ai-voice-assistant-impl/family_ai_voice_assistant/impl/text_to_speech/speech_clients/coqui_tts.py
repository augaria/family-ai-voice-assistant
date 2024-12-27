import tempfile
from TTS.api import TTS
import torch

from family_ai_voice_assistant.core.clients import (
    ClientManager,
    SpeechClient,
    PlaySoundClient
)
from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.clients import WaitableResultClient
from family_ai_voice_assistant.core.helpers.language_manager import (
    LanguageManager
)

from ...configs import CoquiTTSConfig, coqui_tts_language_map


class CoquiTTS(SpeechClient):

    def __init__(self):
        config = ConfigManager().get_instance(CoquiTTSConfig)

        if config is None:
            raise ValueError("CoquiTTSConfig is not set.")
        if config.model is None or config.model == "":
            raise ValueError("CoquiTTSConfig.model is not set.")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self._client = TTS(config.model).to(device)

        if config.speaker_id is not None:
            self._speaker_id = config.speaker_id
        if config.speaker_wav is not None:
            self._speaker_wav = config.speaker_wav
        if self._speaker_id is None and self._speaker_wav is None:
            raise ValueError(
                "CoquiTTSConfig.speaker_id or "
                "CoquiTTSConfig.speaker_wav must be set."
            )

    def speech_async(self, text: str) -> WaitableResultClient:
        language = coqui_tts_language_map[LanguageManager().get()]
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:  # noqa: E501
            if self._speaker_id is not None:
                self._client.tts_to_file(
                    text,
                    speaker=self._speaker_id,
                    language=language,
                    file_path=tmp_file.name
                )
            else:
                self._client.tts_to_file(
                    text,
                    speaker_wav=self._speaker_wav,
                    language=language,
                    file_path=tmp_file.name
                )
            play_sound_client = ClientManager().get_client(PlaySoundClient)
            if play_sound_client is None:
                raise ValueError("PlaySoundClient is not set.")
            return play_sound_client.play_async(tmp_file.name)

    def stop_async(self) -> WaitableResultClient:
        play_sound_client = ClientManager().get_client(PlaySoundClient)
        if play_sound_client is None:
            raise ValueError("PlaySoundClient is not set.")
        return play_sound_client.stop_async()
