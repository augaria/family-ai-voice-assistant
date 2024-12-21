from typing import Dict

from family_ai_voice_assistant.core.tools_engine import (
    tool_function
)
from family_ai_voice_assistant.core.contracts import Language

from family_ai_voice_assistant.core.helpers.common_helpers import (
    get_time_with_timezone
)
from family_ai_voice_assistant.core.utils.program_control import (
    ProgramControl
)
from family_ai_voice_assistant.core.helpers.language_manager import (
    LanguageManager
)


@tool_function
def get_time_and_timezone() -> Dict[str, str]:
    """
    Get time and timezone.
    """
    now = get_time_with_timezone()
    return {
        "time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "timezone": str(now.tzinfo)
    }


@tool_function
def switch_language(language: Language = None):
    """
    Switch language for the conversation between you and the user.

    :param language: Language to switch to, CHS for Chinese, EN for English
    """
    LanguageManager().set(language)


@tool_function
def exit_program():
    """
    Exit the program. The program will stop after the last message from LLM.
    """
    ProgramControl().exit()
