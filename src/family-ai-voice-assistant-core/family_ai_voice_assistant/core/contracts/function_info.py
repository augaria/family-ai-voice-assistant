from dataclasses import dataclass
from typing import List


@dataclass
class ParameterInfo:
    name: str
    description: str
    type: str
    default: str
    is_required: bool
    is_callable: bool = False


@dataclass
class FunctionInfo:
    name: str
    full_name: str
    function_instance: callable
    description: str
    parameters: List[ParameterInfo]
    return_type: str
