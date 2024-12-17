import yaml
from typing import TypeVar, Type, Dict

from ._config_handler import _ConfigHandler


T = TypeVar('T')


class _YamlConfigHandler(_ConfigHandler):

    def __init__(self, yaml_path: str) -> None:
        with open(yaml_path, 'r') as file:
            self._config_data: Dict = yaml.safe_load(file)

    def get_section(self, section_type: Type[T]) -> T:
        section_name = section_type.__name__.replace("Config", "").lower()
        return self._config_data.get(section_name, None)
