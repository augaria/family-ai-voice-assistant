from typing import Set, List, Tuple

from ..utils.singleton_meta import SingletonMeta
from ..contracts import FunctionInfo
from ..helpers.reflection_helpers import RefectionHelpers
from ..configs import ToolsConfig, ConfigManager
from ._tool_functions_registration import _ToolFunctionsRegistration
from ..telemetry import trace
from ..logging import Loggers


def tool_function(function_instance: callable):
    _ToolFunctionsRegistration().register_function(function_instance)
    return function_instance


class IncludeMode:
    all: bool = False
    include: bool = False
    exclude: bool = False


class ToolFunctionsManager(metaclass=SingletonMeta):

    def __init__(self):
        self._config = ConfigManager().get_instance(ToolsConfig)
        self._selected_list = set()
        if (
            self._config is not None
            and self._config.packages is not None
            and len(self._config.packages) > 0
        ):
            for package in self._config.packages:
                RefectionHelpers.import_all_modules(package)
            self._filter_functions_with_selection()

    def get_function_infos(
        self,
        selected_from_config: bool = False
    ) -> List[FunctionInfo]:
        if selected_from_config:
            return list(
                _ToolFunctionsRegistration().selected_functions.values()
            )
        return list(
            _ToolFunctionsRegistration().registered_functions.values()
        )

    @trace()
    def invoke_tool_function(self, name: str, arguments: dict):
        try:
            function_info = (
                _ToolFunctionsRegistration().registered_functions[name]
            )
            valid_args = {param.name for param in function_info.parameters}
            filtered_args = {
                k: v for k, v in arguments.items() if k in valid_args
            }
            Loggers().tool.info(
                f"Invoke tool [{name}] with args: {filtered_args}"
            )
            res = function_info.function_instance(**filtered_args)
            Loggers().tool.info(
                f"Tool [{name}] succeeded. "
                f"Result: {self.truncate_string(str(res), 100)}"
            )
            return res
        except Exception as e:
            Loggers().tool.error(
                f"Tool [{name}] failed. Error: {e}"
            )
            return str(e)

    @staticmethod
    def truncate_string(s: str, limit: int) -> str:
        if len(s) > limit:
            return s[:(limit - 3)] + '...'
        return s

    def _filter_functions_with_selection(self):
        include_mode, functions_set = self._parse_functions_selection()

        for function_info in (
            _ToolFunctionsRegistration().registered_functions.values()
        ):
            if self._is_function_selected(
                function_info.name,
                include_mode,
                functions_set
            ):
                _ToolFunctionsRegistration().select_function(
                    function_info.name
                )

    def _parse_functions_selection(self) -> Tuple[IncludeMode, Set[str]]:
        try:
            include_mode = self._parse_include_mode()
            if include_mode.include:
                return (
                    include_mode,
                    set(self._config.include_functions)
                )
            if include_mode.exclude:
                return (
                    include_mode,
                    set(self._config.exclude_functions)
                )
            return (include_mode, None)
        except Exception as e:
            Loggers().tool.error(f"Failed to parse tools selection: {e}")

    def _parse_include_mode(self) -> IncludeMode:
        res = IncludeMode()
        res.include = (self._config.include_functions is not None)
        res.exclude = (self._config.exclude_functions is not None)
        if res.include and res.exclude:
            raise ValueError(
                "Both include_functions and exclude_functions are set"
            )
        if not res.include and not res.exclude:
            res.all = True
        return res

    @staticmethod
    def _is_function_selected(
        function_name: str,
        include_mode: IncludeMode,
        function_set: Set[str]
    ) -> bool:
        if include_mode.all:
            return True
        if include_mode.include:
            return function_name in function_set
        if include_mode.exclude:
            return function_name not in function_set
