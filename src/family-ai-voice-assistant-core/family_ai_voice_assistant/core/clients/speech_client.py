from abc import ABC, abstractmethod

from .watiable_result_client import WaitableResultClient
from ..contracts import TaskStatus
from ..telemetry import trace


class SpeechClient(ABC):

    @trace()
    def speech(self, text: str) -> TaskStatus:
        return self.speech_async(text).wait()

    def stop(self) -> TaskStatus:
        return self.stop_async().wait()

    @abstractmethod
    def speech_async(self, text: str) -> WaitableResultClient:
        pass

    @abstractmethod
    def stop_async(self) -> WaitableResultClient:
        pass
