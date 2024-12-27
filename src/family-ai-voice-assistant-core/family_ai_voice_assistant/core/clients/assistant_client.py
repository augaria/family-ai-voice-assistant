from abc import ABC, abstractmethod


class AssistantClient(ABC):

    @abstractmethod
    def run(self) -> None:
        pass
