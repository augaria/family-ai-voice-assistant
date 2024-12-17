from .utils.constants_provider import (
    ConstantsProvider,
    Language
)
from .utils.common_utils import get_absolute_path_based_on_reference_file
from .config._config_handler._config_handler_factory import (
    _ConfigHandlerFactory
)


def set_yaml_config_path(path: str):
    _ConfigHandlerFactory.set_yaml_config_path(path)


constants_file_chs = get_absolute_path_based_on_reference_file(
    __file__,
    'resources/constants_chs.json'
)
ConstantsProvider().load_from_file(
    constants_file_chs,
    Language.CHS
)

constants_file_en = get_absolute_path_based_on_reference_file(
    __file__,
    'resources/constants_en.json'
)
ConstantsProvider().load_from_file(
    constants_file_en,
    Language.EN
)
