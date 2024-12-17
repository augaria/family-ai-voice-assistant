import requests

from family_ai_voice_assistant.core.config import ConfigManager
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers

from ..config.bulitin_tools_config import BuiltInFunctionsConfig


def config():
    return ConfigManager().get_instance(BuiltInFunctionsConfig)


@tool_function
def get_weather_info(
    city_adcode: str = None,
    extensions: str = 'base'
):
    """
    Use Amap API to get weather information of a specified city.

    :param city_adcode: City adcode
    :param extensions: 'base' returns current weather, 'all' returns forecast
    """

    if city_adcode is None:
        city_adcode = config().default_city_adcode

    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        'key': config().amap_api_key,
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
            Loggers().tool.warning(f"weather tool failed: {data['info']}")
            return None

    except requests.exceptions.RequestException as e:
        Loggers().tool.warning(f"weather tool HTTP Request failed: {e}")
        return None
