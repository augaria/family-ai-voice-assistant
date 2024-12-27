from ..utils.singleton_meta import SingletonMeta
from ..contracts import Language
from ..configs import GeneralConfig, ConfigManager


class LanguageManager(metaclass=SingletonMeta):

    def __init__(self):
        config = ConfigManager().get_instance(GeneralConfig)
        if config is not None and config.language is not None:
            self._default_language = config.language
        else:
            self._default_language = Language.CHS
        self._runtime_language = self._default_language

    def set(self, language: Language = None):
        if language is None:
            self._runtime_language = self._default_language
        else:
            self._runtime_language = language

    def get(self) -> Language:
        return self._runtime_language
