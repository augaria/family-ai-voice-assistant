from abc import ABC, abstractmethod
import json
import random

from ..telemetry import trace


class GreetingClient(ABC):

    @abstractmethod
    def words(self) -> str:
        pass


class RandomGreetingWordsFromList(GreetingClient):

    def __init__(self):
        from ..config import ConfigManager, GeneralConfig

        self._list = []
        config = ConfigManager().get_instance(GeneralConfig)
        if config is None or config.greeting_words_path is None:
            raise ValueError("Greeting words path is not set.")
        with open(config.greeting_words_path, 'r', encoding='utf-8') as file:
            self._list = json.load(file)

    @trace()
    def words(self) -> str:
        return random.choice(self._list)