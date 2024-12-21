from typing import Dict

from ..utils.singleton_meta import SingletonMeta
from ..contracts import FunctionInfo
from ..helpers.reflection_helpers import RefectionHelpers


class _ToolFunctionsRegistration(metaclass=SingletonMeta):

    def __init__(self):
        self._registered_functions: Dict[str, FunctionInfo] = {}
        self._selected_functions: Dict[str, FunctionInfo] = {}

    def register_function(self, function_instance: callable):
        function_info = RefectionHelpers.parse_function_info(function_instance)
        self._registered_functions[function_info.name] = function_info

    def select_function(self, function_name: str):
        if function_name not in self._registered_functions:
            raise ValueError(
                f"Function [{function_name}] is not registered"
            )
        self._selected_functions[function_name] = (
            self._registered_functions[function_name]
        )

    @property
    def registered_functions(self):
        return self._registered_functions

    @property
    def selected_functions(self):
        return self._selected_functions
