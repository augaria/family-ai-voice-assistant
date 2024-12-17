from abc import ABC, abstractmethod


class PlaySoundClient(ABC):

    @abstractmethod
    def play(self, audio_file: str) -> None:
        pass
