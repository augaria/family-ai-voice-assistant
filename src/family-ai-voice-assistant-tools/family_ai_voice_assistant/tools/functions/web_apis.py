import requests
from typing import Dict, Union

from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers

from ..configs.bulitin_tools_config import BuiltInToolsConfig


def config():
    return ConfigManager().get_instance(BuiltInToolsConfig)


@tool_function
def get_weather_info(
    city_adcode: str = None,
    extensions: str = 'base'
) -> Union[Dict, str]:
    """
    Use Amap API to get weather information of a specified city.

    :param city_adcode: City adcode
    :param extensions: 'base' returns current weather, 'all' returns forecast
    """

    if city_adcode is None or city_adcode == "":
        city_adcode = config().default_city_adcode

    api_key = config().amap_api_key
    if not api_key or api_key == "":
        error_msg = "Amap API key not found"
        Loggers().tool.error(error_msg)
        return error_msg

    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        'key': api_key,
        'city': city_adcode,
        'extensions': extensions,
        'output': "JSON"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == '1':
            return data
        else:
            error_msg = f"weather tool failed: {data['info']}"
            Loggers().tool.error(error_msg)
            return error_msg

    except Exception as e:
        error_msg = f"weather tool failed: {e}"
        Loggers().tool.error(error_msg)
        return error_msg
