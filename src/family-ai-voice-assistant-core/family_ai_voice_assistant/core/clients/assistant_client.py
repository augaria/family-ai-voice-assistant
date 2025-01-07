from abc import ABC, abstractmethod


class AssistantClient(ABC):
    """
    Abstract base class for an assistant client.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Run the assistant client.
        """
        pass
