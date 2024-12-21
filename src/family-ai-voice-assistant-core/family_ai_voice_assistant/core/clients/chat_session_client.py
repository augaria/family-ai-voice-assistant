from abc import abstractmethod
from typing import List
from uuid import uuid4

from ..contracts import ChatRecord
from ..config import ChatSessionConfig, ConfigManager
from ..helpers.common_helpers import get_time_with_timezone


class ChatSessionClient:

    def __init__(self):
        config = ConfigManager().get_instance(ChatSessionConfig)
        self._history: List[ChatRecord] = []
        self._usage = 0
        self._max_usage = config.max_token_per_session
        self._session_id = str(uuid4())

        self._init_prompt = None
        if config.init_prompt_path is not None:
            with open(config.init_prompt_path, 'r', encoding='utf-8') as file:
                self._init_prompt = file.read()
                time_info = get_time_with_timezone()
                self.add_system_message(
                    f"{self._init_prompt}\r\n "
                    f"current time from system: {time_info}, "
                    f"timezone: {time_info.tzinfo}"
                )

    def add_message(
        self,
        message: dict,
        serilizable: bool = False,
        wav_bytes: bytes = None
    ):
        record = ChatRecord(
            session_id=self._session_id,
            message=message,
            timestamp=get_time_with_timezone(),
            wav_bytes=wav_bytes,
            serilizable=serilizable
        )

        self._history.append(record)

    def set_usage(self, usage: int):
        self._usage = usage

    def update_session(self):
        if self._max_usage > 0 and self._usage >= (int)(0.9 * self._max_usage):
            self._history.clear()
            if self._init_prompt is not None:
                self.add_system_message(self._init_prompt)

    @property
    def messages(self) -> List[dict]:
        return [record.message for record in self._history]

    @property
    def history(self) -> List[ChatRecord]:
        return self._history

    @abstractmethod
    def add_system_message(self, content: str):
        pass

    @abstractmethod
    def add_user_message(self, content: str, wav_bytes: bytes):
        pass

    @abstractmethod
    def add_assistant_message(self, content: str):
        pass

    @abstractmethod
    def add_tool_message(
        self,
        tool_name: str,
        content: str,
        tool_call_id: str = None
    ):
        pass
