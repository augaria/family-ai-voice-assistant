from typing import Type, TypeVar, Any
from dataclasses import fields, dataclass

from ._config_handlers._config_handler_factory import _ConfigHandlerFactory
from ._config_handlers._config_handler import _ConfigHandler
from ..utils.global_instance_manager import GlobalInstanceManager


T = TypeVar('T')


def from_dict(data_class: Type, data: Any):
    if isinstance(data, dict):
        fieldtypes = {f.name: f.type for f in fields(data_class)}
        return data_class(
            **{f: from_dict(fieldtypes[f], data[f]) for f in data}
        )
    elif isinstance(data, list):
        return [from_dict(data_class.__args__[0], item) for item in data]
    else:
        return data


@dataclass
class Config:

    @classmethod
    def populate(config_type: Type[T]) -> T:
        config_handler: _ConfigHandler = _ConfigHandlerFactory.get_instance()
        if config_handler is None:
            return None
        section_data = config_handler.get_section(config_type)
        return config_type.from_dict(section_data)

    @classmethod
    def from_dict(config_type: Type[T], data: Any) -> T:
        return from_dict(config_type, data)


class ConfigManager(GlobalInstanceManager):

    def get_instance(
        self,
        config_type: Type[T]
    ) -> T:
        config = super()._get_instance(
            identifier=config_type,
            config_type=config_type
        )
        if config is not None:
            return config

        super()._remove_instance(identifier=config_type)
        return super()._get_instance(
            identifier=config_type,
            config_type=config_type
        )

    def _create_instance(self, config_type: Type[Config]) -> Config:
        return config_type.populate()
