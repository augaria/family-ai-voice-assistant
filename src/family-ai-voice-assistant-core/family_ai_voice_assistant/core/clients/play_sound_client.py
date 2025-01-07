from abc import ABC, abstractmethod

from .watiable_result_client import WaitableResultClient
from ..contracts import TaskStatus


class PlaySoundClient(ABC):
    """
    Abstract base class for a client that plays sounds.
    """

    def play(self, audio_file: str) -> TaskStatus:
        """
        Play an audio file synchronously.

        :param audio_file: The path to the audio file.
        :return: The status of the play task.
        """
        return self.play_async(audio_file).wait()

    def stop(self) -> TaskStatus:
        """
        Stop playing audio synchronously.

        :return: The status of the stop task.
        """
        return self.stop_async().wait()

    @abstractmethod
    def play_async(self, audio_file: str) -> WaitableResultClient:
        """
        Play an audio file asynchronously.

        :param audio_file: The path to the audio file.
        :return: A client to wait for the task completion.
        """
        pass

    @abstractmethod
    def stop_async(self) -> WaitableResultClient:
        """
        Stop playing audio asynchronously.

        :return: A client to wait for the task completion.
        """
        pass
