from abc import ABC, abstractmethod

from .watiable_result_client import WaitableResultClient
from ..contracts import TaskStatus
from ..telemetry import trace


class SpeechClient(ABC):
    """
    Abstract base class for a client that handles speech synthesis.
    """

    @trace()
    def speech(self, text: str) -> TaskStatus:
        """
        Synthesize speech from text synchronously.

        :param text: The text to synthesize.
        :return: The status of the speech task.
        """
        return self.speech_async(text).wait()

    def stop(self) -> TaskStatus:
        """
        Stop speech synthesis synchronously.

        :return: The status of the stop task.
        """
        return self.stop_async().wait()

    @abstractmethod
    def speech_async(self, text: str) -> WaitableResultClient:
        """
        Synthesize speech from text asynchronously.

        :param text: The text to synthesize.
        :return: A client to wait for the task completion.
        """
        pass

    @abstractmethod
    def stop_async(self) -> WaitableResultClient:
        """
        Stop speech synthesis asynchronously.

        :return: A client to wait for the task completion.
        """
        pass
