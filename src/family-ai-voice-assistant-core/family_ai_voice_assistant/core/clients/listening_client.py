from abc import ABC, abstractmethod
from typing import Any, List, Union

from speech_recognition import Recognizer, Microphone, exceptions, AudioData

from ..configs import ConfigManager, SpeechRecognitionConfig
from ..telemetry import trace
from ..logging import Loggers


class ListeningClient(ABC):
    """
    Abstract base class for a listening client.
    """

    @abstractmethod
    def listen(self) -> Union[AudioData, Any]:
        """
        Listen for audio input and return audio data.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_wav_from_audio(audio: Union[AudioData, Any]) -> bytes:
        """
        Convert audio data to WAV format.

        :param audio: The audio data to convert.
        :return: The WAV byte data.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_wav_from_audio_list(
        audio_list: List[Union[AudioData, Any]]
    ) -> bytes:
        """
        Convert a list of audio data to WAV format.

        :param audio_list: The list of audio data to convert.
        :return: The WAV byte data.
        """
        pass


class SpeechRecognitionListening(ListeningClient):

    def __init__(self):
        self._config = ConfigManager().get_instance(
            SpeechRecognitionConfig
        )
        if self._config is None:
            raise ValueError("SpeechRecognitionConfig is not set.")

        self._agent = Recognizer()
        self._agent.pause_threshold = self._config.pause_threshold
        if self._config.energy_threshold:
            self._agent.dynamic_energy_threshold = False
            self._agent.energy_threshold = self._config.energy_threshold
        self._source = Microphone()
        self._timeout = self._config.timeout if self._config.timeout else None
        self._phrase_time_limit = self._config.phrase_time_limit

    @trace()
    def listen(self) -> AudioData:
        try:
            with self._source as source:
                if not self._config.energy_threshold:
                    self._agent.adjust_for_ambient_noise(source)
                return self._agent.listen(
                    self._source,
                    timeout=self._timeout,
                    phrase_time_limit=self._phrase_time_limit
                )
        except exceptions.WaitTimeoutError:
            Loggers().listening.warning("Listening timeout")
            return None

    @staticmethod
    def get_wav_from_audio(audio: Union[AudioData, Any]) -> bytes:
        if not isinstance(audio, AudioData):
            Loggers().listening.warning(
                "AudioData format is required to get wav"
            )
            return None
        return audio.get_wav_data()

    @staticmethod
    def get_wav_from_audio_list(
        audio_list: List[Union[AudioData, Any]]
    ) -> bytes:
        audio_data_list: List[AudioData] = [
            audio for audio in audio_list if isinstance(audio, AudioData)
        ]
        if len(audio_data_list) == 0:
            Loggers().listening.warning(
                "AudioData format is required to get wav"
            )
            return None
        combined_frame_data = b''.join(
            audio.frame_data for audio in audio_data_list
        )
        if len(audio_data_list) == 0:
            return None
        return AudioData(
            combined_frame_data,
            audio_data_list[0].sample_rate,
            audio_data_list[0].sample_width
        ).get_wav_data()
