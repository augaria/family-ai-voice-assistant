from dataclasses import dataclass

from family_ai_voice_assistant.core.configs import Config


@dataclass
class BuiltInToolsConfig(Config):
    # local_apis
    mongo_connection_str: str = None
    mongo_database: str = None
    english_word_list_collection: str = None
    chinese_phrase_list_collection: str = None
    memo_list_collection: str = None

    # search
    google_search_api_key: str = None
    bing_subscription_key: str = None
    bing_search_endpoint: str = None

    # web_apis
    amap_api_key: str = None
    default_city_adcode: str = None
