from datetime import datetime
import pytz
from enum import Enum
import threading
from typing import Any, List, Dict

from apscheduler.schedulers.background import BackgroundScheduler

from family_ai_voice_assistant.core.helpers.common_helpers import (
    get_time_with_timezone
)
from family_ai_voice_assistant.core.helpers.mongodb_manager import (
    MongoDbManager
)
from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.helpers.constants_provider import (
    ConstantsProvider
)
from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.logging import Loggers

from ..configs.bulitin_tools_config import BuiltInToolsConfig


class MongoResult(Enum):
    INSERTED = "inserted"
    UPDATED = "updated"
    FAILED = "failed"
    FOUND = "found"
    NOT_FOUND = "not_found"


def config():
    return ConfigManager().get_instance(BuiltInToolsConfig)


def mongo_db():
    client = MongoDbManager().get_instance(config().mongo_connection_str)
    return client[config().mongo_database]


def insert_to_mongo(
    collection_name: str,
    data: dict,
    unique_field: str = None
) -> MongoResult:
    collection = mongo_db()[collection_name]

    if unique_field is not None:
        result = collection.update_one(
            {unique_field: data[unique_field]},
            {'$inc': {'hit_count': 1}},
            upsert=False
        )
        if result.modified_count > 0:
            return MongoResult.UPDATED

    data['hit_count'] = 1
    data['reviewed_count'] = 0
    now = get_time_with_timezone().isoformat()
    data['timestamp'] = now
    data['last_reviewed'] = now
    collection.insert_one(data)
    return MongoResult.INSERTED


def get_mongo_items(
    collection_name: str,
    target_field: str,
    target_value: Any
) -> List[Dict[str, Any]]:
    collection = mongo_db()[collection_name]
    items = collection.find({target_field: target_value})
    items = list(items)
    serializable_items = [
        {key: value for key, value in item.items() if key != '_id'}
        for item in items
    ]
    return serializable_items


def get_min_last_reviewed_and_update(
    collection_name: str,
    count: int
) -> List[Dict[str, Any]]:
    collection = mongo_db()[collection_name]
    items = collection.find().sort("last_reviewed", 1).limit(count)
    items = list(items)
    for item in items:
        collection.update_one(
            {"_id": item["_id"]},
            {"$set": {"last_reviewed": get_time_with_timezone().isoformat()}}
        )
    serializable_items = [
        {key: value for key, value in item.items() if key != '_id'}
        for item in items
    ]
    return serializable_items


def get_collection_count(collection_name: str):
    collection = mongo_db()[collection_name]
    return collection.count_documents({})


@tool_function
def add_to_english_word_list(
    english_word: str,
    part_of_speech: str,
    chinese_explanation: str,
    example_sentence: str
):
    """
    Add new English words to the vocabulary list.

    :param english_word: English word
    :param part_of_speech: Part of speech
    :param chinese_explanation: 中文释义
    :param example_sentence: Example sentence
    """

    try:
        arguments = {
            "english_word": english_word,
            "part_of_speech": part_of_speech,
            "chinese_explanation": chinese_explanation,
            "example_sentence": example_sentence
        }
        res = insert_to_mongo(
            collection_name=config().english_word_list_collection,
            data=arguments,
            unique_field='english_word'
        )

        if res == MongoResult.UPDATED:
            Loggers().tool.info(f"Duplicated word detected: {english_word}")
            return {
                "result": (
                    "You already added that word before. "
                    "Just increased the hit-count. "
                    f"Input parameters {arguments}"
                )
            }
        return {
            "result": f"New word addition completed. "
            f"Input parameters: {arguments}"
        }

    except Exception as e:
        return str(e)


@tool_function
def review_english_words(count: int = 3):
    """
    Get certain number of English words from the list to review.

    :param count: Number of words to review
    """

    return get_min_last_reviewed_and_update(
        config().english_word_list_collection,
        count
    )


@tool_function
def count_english_word_list():
    """
    Count the number of English words in the list.
    """

    return get_collection_count(config().english_word_list_collection)


@tool_function
def add_to_chinese_phrase_list(
    phrase: str,
    pinyin: str,
    explanation: str,
    example_sentence: str,
    source: str = ""
):
    """
    添加新的中文词语到词语本.

    :param phrase: 中文词语
    :param pinyin: 拼音
    :param explanation: 解释
    :param example_sentence: 例句
    :param source: 出处或者典故
    """
    try:

        arguments = {
            "phrase": phrase,
            "pinyin": pinyin,
            "explanation": explanation,
            "example_sentence": example_sentence,
            "source": source
        }

        res = insert_to_mongo(
            collection_name=config().chinese_phrase_list_collection,
            data=arguments,
            unique_field='phrase'
        )

        if res == MongoResult.UPDATED:
            Loggers().tool.info(f"Duplicated phrase detected: {phrase}")
            return {
                "result":
                    "You already added that phrase before. "
                    "Just increased the hit-count. "
                    f"Input parameters {arguments}"
            }
        return {
            "result":
                "Chinese phrase addition completed. "
                f"Input parameters: {arguments}"
        }

    except Exception as e:
        return str(e)


@tool_function
def review_chinese_phrases(count: int = 3):
    """
    Get certain number of Chinese phrases from the list to review.

    :param count: Number of phrases to review
    """

    return get_min_last_reviewed_and_update(
        config().chinese_phrase_list_collection,
        count
    )


@tool_function
def count_chinese_phrase_list():
    """
    Count the number of Chinese phrases in the list.
    """

    return get_collection_count(config().chinese_phrase_list_collection)


@tool_function
def add_to_memo(date: str, content: str, hour: str = ""):
    """
    Add memo to the memo list.

    :param date: Target date, string format %Y-%m-%d
    :param content: Memo content
    :param hour: Target hour, default None
    """

    try:
        arguments = {
            "date": date,
            "content": content,
            "hour": hour
        }
        insert_to_mongo(
            collection_name=config().memo_list_collection,
            data=arguments
        )

        return {
            "result":
                "Memo addition completed. "
                f"Input parameters: {arguments}"
        }

    except Exception as e:
        Loggers().tool.error(f"Error: {e}")
        return str(e)


@tool_function
def get_memos(date: str) -> List[Dict[str, Any]]:
    """
    Get memos for the target date.

    :param date: Target date, string format %Y-%m-%d
    """

    return get_mongo_items(
        config().memo_list_collection,
        'date',
        date
    )


@tool_function
def count_down_timer(seconds: int, message: str = "") -> Any:
    """
    Countdown function, will alert user when finished.

    :param seconds: Countdown seconds
    :param message: message to say when countdown finished, default None
    """

    try:
        from family_ai_voice_assistant.core.clients import (
            ClientManager,
            SpeechClient
        )
        speech_client = ClientManager().get_client(SpeechClient)
        if speech_client is None:
            error_msg = "Speech client not found. Can't alert user."
            Loggers().tool.error(error_msg)
            return error_msg

        if message is not None and message != "":
            count_down_message = message
        else:
            count_down_message = ConstantsProvider().get(
                'COUNTDOWN_MESSAGE'
            )
        timer = threading.Timer(
            seconds,
            speech_client.speech,
            args=(count_down_message,)
        )
        timer.start()
    except Exception as e:
        Loggers().tool.error(f"Error: {e}")
        return str(e)


@tool_function
def alarm_timer(target_time_str: str, message: str = "") -> Any:
    """
    Alarm function, will alert user at specified time.

    :param target_time_str: Alarm time, string format %H:%M:%S
    :param message: message to say when target time reached, default None
    """
    now = get_time_with_timezone()
    scheduler = BackgroundScheduler(timezone=str(now.tzinfo))

    try:
        from family_ai_voice_assistant.core.clients import (
            ClientManager,
            SpeechClient
        )
        speech_client = ClientManager().get_client(SpeechClient)
        if speech_client is None:
            error_msg = "Speech client not found. Can't alert user."
            Loggers().tool.error(error_msg)
            return error_msg

        now = get_time_with_timezone()
        today_str = now.strftime('%Y-%m-%d')
        full_target_time_str = f"{today_str} {target_time_str}"
        target_time = datetime.strptime(
            full_target_time_str,
            '%Y-%m-%d %H:%M:%S'
        )
        target_time = pytz.timezone(str(now.tzinfo)).localize(
            target_time
        )

        if target_time > now:
            if message is not None and message != "":
                alarm_message = message
            else:
                alarm_message = ConstantsProvider().get(
                    'ALARM_MESSAGE'
                ).format(
                    time=target_time_str
                )
            scheduler.add_job(
                speech_client.speech,
                'date',
                run_date=target_time,
                args=(alarm_message,)
            )
            scheduler.start()
        else:
            speech_client.speech(ConstantsProvider().get('PAST_TIME_MESSAGE'))
    except Exception as e:
        Loggers().tool.error(f"Error: {e}")
        return str(e)
