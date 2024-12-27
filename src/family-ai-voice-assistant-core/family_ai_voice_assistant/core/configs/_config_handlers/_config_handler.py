from abc import ABC, abstractmethod
from typing import Dict


class _ConfigHandler(ABC):

    @abstractmethod
    def get_section(self, section_type: type) -> Dict:
        pass
