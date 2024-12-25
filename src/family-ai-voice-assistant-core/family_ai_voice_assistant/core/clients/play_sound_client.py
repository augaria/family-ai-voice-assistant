from abc import ABC, abstractmethod

from .watiable_result_client import WaitableResultClient
from ..contracts import TaskStatus


class PlaySoundClient(ABC):

    def play(self, audio_file: str) -> TaskStatus:
        return self.play_async(audio_file).wait()

    def stop(self) -> TaskStatus:
        return self.stop_async().wait()

    @abstractmethod
    def play_async(self, audio_file: str) -> WaitableResultClient:
        pass

    @abstractmethod
    def stop_async(self) -> WaitableResultClient:
        pass
