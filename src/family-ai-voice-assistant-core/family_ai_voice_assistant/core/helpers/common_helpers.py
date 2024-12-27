import os
from datetime import datetime

import pytz
from tzlocal import get_localzone

from ..configs import ConfigManager, GeneralConfig


def get_time_with_timezone() -> datetime:
    now = datetime.now()

    config = ConfigManager().get_instance(GeneralConfig)
    if config is not None and config.timezone:
        timezone = pytz.timezone(config.timezone)
    else:
        timezone = get_localzone()
    return now.astimezone(timezone)


def get_absolute_path_based_on_reference_file(

    file_path: str,
    relative_path: str
) -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(file_path)), relative_path
    )
