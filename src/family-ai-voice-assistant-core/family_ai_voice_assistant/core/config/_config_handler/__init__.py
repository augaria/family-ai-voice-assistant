from abc import ABC, abstractmethod
from typing import Any


class ConfigHandler(ABC):

    @abstractmethod
    def get_value(key: str) -> Any:
        pass
