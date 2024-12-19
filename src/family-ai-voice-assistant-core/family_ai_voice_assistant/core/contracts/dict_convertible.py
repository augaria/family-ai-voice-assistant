from dataclasses import dataclass, fields, is_dataclass
from typing import Dict, Type, TypeVar


T = TypeVar('T', bound='DictConvertible')


@dataclass
class DictConvertible:
    def to_dict(self) -> Dict:
        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, DictConvertible):
                result[field.name] = value.to_dict()
            elif isinstance(value, list):
                result[field.name] = [
                    item.to_dict() if isinstance(item, DictConvertible)
                    else item for item in value
                ]
            elif isinstance(value, dict):
                result[field.name] = {
                    key: val.to_dict() if isinstance(val, DictConvertible)
                    else val for key, val in value.items()
                }
            else:
                result[field.name] = value
        return result

    @classmethod
    def from_dict(cls: Type[T], data: Dict) -> T:
        init_kwargs = {}
        for field in fields(cls):
            if field.name in data:
                value = data[field.name]
                if is_dataclass(field.type) and issubclass(
                    field.type,
                    DictConvertible
                ):
                    init_kwargs[field.name] = field.type.from_dict(value)
                elif isinstance(value, list):
                    init_kwargs[field.name] = [
                        field.type.__args__[0].from_dict(
                            item) if isinstance(item, dict) else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    init_kwargs[field.name] = {
                        key: field.type.__args__[1].from_dict(
                            val) if isinstance(val, dict) else val
                        for key, val in value.items()
                    }
                else:
                    init_kwargs[field.name] = value
        return cls(**init_kwargs)
