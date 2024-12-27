from enum import Enum


class Language(str, Enum):
    CHS = 'CHS'
    EN = 'EN'


class TaskStatus(str, Enum):
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    CANCELLED = 'Cancelled'


class LoggerName(str, Enum):
    WAKER = 'Waker'
    LLM = 'LLM'
    CHAT_SESSION = 'ChatSession'
    HISTORY_STORE = 'HistoryStore'
    FILE_STORE = 'FileStore'
    LISTENING = 'Listening'
    RECOGNITION = 'Recognition'
    PLAY_SOUND = 'PlaySound'
    SPEECH = 'Speech'
    GREETING = 'Greeting'
    WAITABLE_RESULT = 'WaitableResult'
    TOOL = 'Tool'
    ASSISTANT = 'Assistant'
    UTILS = 'Utils'
