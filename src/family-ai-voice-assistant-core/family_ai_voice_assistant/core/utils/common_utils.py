import os
from datetime import datetime

import pytz

from ..config import ConfigManager, GeneralConfig


def get_time_with_timezone() -> datetime:
    config = ConfigManager().get_instance(GeneralConfig)
    now = datetime.now()
    timezone = pytz.timezone(config.timezone)
    return now.astimezone(timezone)


def get_absolute_path_based_on_reference_file(
    file_path: str,
    relative_path: str
) -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(file_path)), relative_path
    )
