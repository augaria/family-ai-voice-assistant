import pvporcupine
import pyaudio
import struct

from family_ai_voice_assistant.core.clients import VoiceWaker
from family_ai_voice_assistant.core.configs import ConfigManager

from ...configs import PicovoiceConfig


class PicovoiceWaker(VoiceWaker):

    def __init__(self):

        config = ConfigManager().get_instance(PicovoiceConfig)
        if config is None:
            raise ValueError("PicovoiceConfig is not set.")
        self._agent = pvporcupine.create(
            access_key=config.api_key,
            model_path=config.model_path,
            keyword_paths=config.keyword_paths
        )

        myaudio = pyaudio.PyAudio()
        self._stream = myaudio.open(
            input_device_index=None,
            rate=self._agent.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self._agent.frame_length
        )

    def check(self) -> bool:
        audio_obj = self._stream.read(
            self._agent.frame_length,
            exception_on_overflow=False
        )
        audio_obj_unpacked = struct.unpack_from(
            "h" * self._agent.frame_length,
            audio_obj
        )
        res = self._agent.process(audio_obj_unpacked) >= 0
        return res
