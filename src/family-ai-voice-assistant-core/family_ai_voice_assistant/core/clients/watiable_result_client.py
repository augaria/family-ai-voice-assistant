from abc import ABC, abstractmethod

from ..contracts import TaskStatus


class WaitableResultClient(ABC):
    """
    Abstract base class for a client that handles waitable results.
    """

    @abstractmethod
    def wait(self) -> TaskStatus:
        """
        Wait for the result of an asynchronous task.

        :return: The status of the task.
        """
        pass
