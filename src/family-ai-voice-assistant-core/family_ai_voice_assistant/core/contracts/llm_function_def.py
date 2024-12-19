from dataclasses import dataclass, field
from typing import List, Dict, Type, TypeVar

from .dict_convertible import DictConvertible
from .function_info import FunctionInfo


T = TypeVar('T', bound='LLMFunctionDefBase')


@dataclass
class ParamProperty(DictConvertible):
    description: str
    type: str


@dataclass
class Parameters(DictConvertible):
    type: str = "object"
    properties: Dict[str, ParamProperty] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)


@dataclass
class LLMFunctionDefBase(DictConvertible):
    name: str
    description: str
    parameters: Parameters

    @classmethod
    def from_function_info(cls: Type[T], function_info: FunctionInfo) -> T:
        properties = {}
        required = []

        for param in function_info.parameters:
            properties[param.name] = ParamProperty(
                description=param.description,
                type=param.type
            )
            if param.is_required:
                required.append(param.name)

        return cls(
            name=function_info.name,
            description=function_info.description,
            parameters=Parameters(
                properties=properties,
                required=required
            )
        )
