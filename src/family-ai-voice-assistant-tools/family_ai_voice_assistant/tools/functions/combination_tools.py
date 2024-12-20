from family_ai_voice_assistant.core.utils.common_utils import (
    get_time_with_timezone
)
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)

from .local_apis import get_memos, review_chinese_phrases, review_english_words
from .search import bing_top_news


@tool_function
def daily_report(famous_saying: str) -> str:
    """
    Generate daily report for the user.

    :param famous_saying: Randomly select an educational quote for children from either Chinese or foreign sources and provide an explanation.  # noqa: E501
    """

    try:
        now = get_time_with_timezone()
        today_str = now.strftime('%Y-%m-%d')

        memos = get_memos(today_str)
        english_words = review_english_words(2)
        chinese_phrases = review_chinese_phrases(2)
        top_news = bing_top_news()

        report = (
            f"date: {today_str}\n"
            f"memos: {memos}\n"
            f"english words to review: {english_words}\n"
            f"chinese phrases to review: {chinese_phrases}\n"
            f"famous saying: {famous_saying}\n"
            f"top news: {top_news}"
        )

        return report

    except Exception as e:
        return str(e)
