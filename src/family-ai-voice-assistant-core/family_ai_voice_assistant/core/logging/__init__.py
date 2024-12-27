from logging import Logger

from .logger_manager import LoggerManager
from ..contracts import LoggerName
from ..utils.singleton_meta import SingletonMeta
from ._ai_assistant_logger import colored_print  # noqa: F401
from colorama import Fore  # noqa: F401


class Loggers(metaclass=SingletonMeta):

    @property
    def assistant(self) -> Logger:
        return LoggerManager().get_instance(LoggerName.ASSISTANT)

    @property
    def tool(self):
        return LoggerManager().get_instance(LoggerName.TOOL)

    @property
    def waker(self):
        return LoggerManager().get_instance(LoggerName.WAKER)

    @property
    def listening(self):
        return LoggerManager().get_instance(LoggerName.LISTENING)

    @property
    def llm(self):
        return LoggerManager().get_instance(LoggerName.LLM)

    @property
    def chat_session(self):
        return LoggerManager().get_instance(LoggerName.CHAT_SESSION)

    @property
    def file_store(self):
        return LoggerManager().get_instance(LoggerName.FILE_STORE)

    @property
    def history_store(self):
        return LoggerManager().get_instance(LoggerName.HISTORY_STORE)

    @property
    def recognition(self):
        return LoggerManager().get_instance(LoggerName.RECOGNITION)

    @property
    def play_sound(self):
        return LoggerManager().get_instance(LoggerName.PLAY_SOUND)

    @property
    def speech(self):
        return LoggerManager().get_instance(LoggerName.SPEECH)

    @property
    def greeting(self):
        return LoggerManager().get_instance(LoggerName.GREETING)

    @property
    def waitable_result(self):
        return LoggerManager().get_instance(LoggerName.WAITABLE_RESULT)

    @property
    def utils(self):
        return LoggerManager().get_instance(LoggerName.UTILS)
