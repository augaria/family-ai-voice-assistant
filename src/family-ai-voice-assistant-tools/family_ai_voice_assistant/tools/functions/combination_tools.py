from typing import Dict, Union

from family_ai_voice_assistant.core.helpers.common_helpers import (
    get_time_with_timezone
)
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers

from .local_apis import get_memos, review_chinese_phrases, review_english_words
from .search import bing_top_news
from .web_apis import get_weather_info


@tool_function
def daily_report(famous_saying: str) -> Union[Dict, str]:
    """
    Generate daily report for the user.

    :param famous_saying: Randomly select an educational quote for children from either Chinese or foreign sources and provide an explanation.  # noqa: E501
    """

    try:
        now = get_time_with_timezone()
        today_str = now.strftime('%Y-%m-%d')

        weather_info = get_weather_info()
        memos = get_memos(today_str)
        english_words = review_english_words(2)
        chinese_phrases = review_chinese_phrases(2)
        top_news = bing_top_news()

        report = {
            "date": today_str,
            "weather": weather_info,
            "memos": memos,
            "english words to review": english_words,
            "chinese phrases to review": chinese_phrases,
            "famous saying": famous_saying,
            "top news": top_news
        }

        return report

    except Exception as e:
        error_msg = f"daily report failed: {e}"
        Loggers().tool.error(error_msg)
        return error_msg
