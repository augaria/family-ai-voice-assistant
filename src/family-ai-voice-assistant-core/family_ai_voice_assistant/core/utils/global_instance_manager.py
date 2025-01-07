import threading
from typing import Dict, Any, TypeVar
from abc import abstractmethod

from .singleton_meta import SingletonMeta


T = TypeVar('T')


class GlobalInstanceManager(metaclass=SingletonMeta):

    def __init__(self):
        self.__instances: Dict[Any, T] = {}
        self.__lock = threading.Lock()

    @abstractmethod
    def get_instance(self, **kwargs) -> T:
        pass

    @abstractmethod
    def _create_instance(self, **kwargs) -> T:
        pass

    def _remove_instance(self, identifier: Any):
        with self.__lock:
            if identifier in self.__instances:
                del self.__instances[identifier]

    def _get_instance(
        self,
        identifier: Any,
        **kwargs
    ) -> T:
        if identifier in self.__instances:
            return self.__instances[identifier]
        with self.__lock:
            if identifier in self.__instances:
                return self.__instances[identifier]

            instance = self._create_instance(**kwargs)

            self.__instances[identifier] = instance
            return instance

    def _add_instance(self, identifier: Any, instance: T):
        with self.__lock:
            self.__instances[identifier] = instance
