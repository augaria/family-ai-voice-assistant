import json

from ..utils.singleton_meta import SingletonMeta
from ..contracts import Language
from ..logging import Loggers
from .language_manager import LanguageManager


class ConstantsProvider(metaclass=SingletonMeta):

    constants = {
        Language.CHS: {},
        Language.EN: {},
    }

    def load_from_file(self, file_path: str, language: Language):
        with open(file_path, 'r') as file:
            consts: dict = json.load(file)
            repeated_keys = set(
                (self.constants[language].keys()) &
                set(consts.keys())
            )

        if repeated_keys:
            error_message = f"Repeated keys: {repeated_keys}"
            Loggers().utils.error(error_message)
            raise ValueError(error_message)
        self.constants[language].update(consts)

    def get(self, key: str) -> str:
        return self.constants[LanguageManager().get()][key]
