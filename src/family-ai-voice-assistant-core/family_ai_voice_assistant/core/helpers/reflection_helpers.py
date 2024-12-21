from typing import get_origin
import importlib
import pkgutil
import inspect
import docstring_parser

from ..contracts import FunctionInfo, ParameterInfo
from ..logging import Loggers


def python_type_to_json_type(py_type):
    if get_origin(py_type) is not None:
        py_type = get_origin(py_type)

    if py_type in [int, float]:
        return 'number'
    elif py_type in [str]:
        return 'string'
    elif py_type in [bool]:
        return 'boolean'
    elif py_type in [list, tuple, set]:
        return 'array'
    elif py_type in [dict]:
        return 'object'
    else:
        return 'string'


class RefectionHelpers:

    @staticmethod
    def parse_function_info(func: callable):
        signature = inspect.signature(func)
        docstring = inspect.getdoc(func)
        parsed_docstring = docstring_parser.parse(docstring)

        parameters = []
        docstring_params = {p.arg_name: p for p in parsed_docstring.params}

        for param_name, param_info in signature.parameters.items():
            param_type = python_type_to_json_type(param_info.annotation)
            param_desc = None
            if param_name in docstring_params:
                param_desc = docstring_params[param_name].description
            param_default = (
                param_info.default
                if param_info.default is not inspect.Parameter.empty
                else None
            )
            is_required = param_default is None
            is_callable = (param_info.annotation == callable)

            parameters.append(ParameterInfo(
                name=param_name,
                description=param_desc,
                type=param_type,
                default=param_default,
                is_required=is_required,
                is_callable=is_callable
            ))

        return FunctionInfo(
            name=func.__name__,
            full_name=f"{func.__module__}.{func.__name__}",
            function_instance=func,
            description=parsed_docstring.short_description,
            parameters=parameters,
            return_type=python_type_to_json_type(signature.return_annotation)
        )

    @staticmethod
    def import_all_modules(package_name):
        try:
            package = importlib.import_module(package_name)
        except ImportError as e:
            Loggers().utils.error(f"Error importing {package_name}: {e}")
            return

        for _, module_name, is_pkg in pkgutil.walk_packages(
            package.__path__, package.__name__ + "."
        ):
            try:
                importlib.import_module(module_name)
            except ImportError as e:
                Loggers().utils.error(
                    f"Error importing module {module_name}: {e}"
                )
