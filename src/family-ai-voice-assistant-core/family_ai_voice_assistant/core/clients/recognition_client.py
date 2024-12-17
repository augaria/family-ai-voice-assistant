from abc import ABC, abstractmethod
from typing import Any, Union

from speech_recognition import AudioData


class RecognitionClient(ABC):

    @abstractmethod
    def recognize(self, audio: Union[AudioData, Any]) -> str:
        pass
