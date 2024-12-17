from abc import ABC, abstractmethod

from ..contracts import TaskStatus


class WaitableResultClient(ABC):

    @abstractmethod
    def wait(self) -> TaskStatus:
        pass
