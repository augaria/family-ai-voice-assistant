from .configs import set_yaml_config_path  # noqa: F401
from .helpers.constants_provider import (
    ConstantsProvider,
    Language
)
from .helpers.common_helpers import (
    get_absolute_path_based_on_reference_file
)


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
