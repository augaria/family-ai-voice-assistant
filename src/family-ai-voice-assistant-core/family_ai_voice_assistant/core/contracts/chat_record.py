from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from .dict_convertible import DictConvertible


@dataclass
class ChatRecord(DictConvertible):
    session_id: str
    message: Dict[str, str]
    timestamp: datetime
    wav_bytes: bytes = None
    serilizable: bool = False


@dataclass
class SerilizableChatRecord(DictConvertible):
    session_id: str
    role: str
    name: str
    message_content: str
    timestamp: datetime
    additional_properties: Dict[str, str]
    wav_file_path: bytes = None
