from abc import ABC, abstractmethod
from typing import Any, Union

from speech_recognition import AudioData


class RecognitionClient(ABC):
    """
    Abstract base class for a client that recognizes speech.
    """

    @abstractmethod
    def recognize(self, audio: Union[AudioData, Any]) -> str:
        """
        Recognize speech from audio data.

        :param audio: The audio data to recognize.
        :return: The recognized text.
        """
        pass
