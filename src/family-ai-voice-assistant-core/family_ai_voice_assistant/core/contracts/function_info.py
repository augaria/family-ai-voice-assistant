from dataclasses import dataclass, field
from typing import List

from .dict_convertible import DictConvertible


@dataclass
class ParameterInfo(DictConvertible):
    name: str
    description: str
    type: str
    default: str
    is_required: bool
    is_callable: bool = False


@dataclass
class FunctionInfo(DictConvertible):
    name: str
    full_name: str
    function_instance: callable
    description: str
    parameters: List[ParameterInfo] = field(default_factory=list)
    return_type: str = None
