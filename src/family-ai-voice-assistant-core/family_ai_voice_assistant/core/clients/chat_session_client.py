from abc import abstractmethod
from typing import List
from uuid import uuid4

from jinja2 import Template
from ..contracts import ChatRecord
from ..configs import ChatSessionConfig, GeneralConfig, ConfigManager
from ..helpers.common_helpers import get_time_with_timezone


class ChatSessionClient:
    """
    Manages a chat session, including message history and session state.
    """

    def __init__(self):
        config = ConfigManager().get_instance(ChatSessionConfig)
        self._history: List[ChatRecord] = []
        self._usage = 0
        self._max_usage = config.max_token_per_session
        self._session_id = str(uuid4())

        self._init_prompt = None
        if config.init_prompt_path is not None:
            with open(config.init_prompt_path, 'r', encoding='utf-8') as file:
                template = Template(file.read())
                general_config = ConfigManager().get_instance(GeneralConfig)
                self._init_prompt = template.render(
                    bot_name=general_config.bot_name,
                    user_name=general_config.user_name,
                    city=general_config.city
                )
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
        """
        Add a message to the session history.

        :param message: The message content as a dictionary.
        :param serilizable: Whether the message should be serialized.
        :param wav_bytes: Optional audio data associated with the message.
        """
        record = ChatRecord(
            session_id=self._session_id,
            message=message,
            timestamp=get_time_with_timezone(),
            wav_bytes=wav_bytes,
            serilizable=serilizable
        )

        self._history.append(record)

    def set_usage(self, usage: int):
        """
        Set the current usage of the session.

        :param usage: The number of tokens used in the session.
        """
        self._usage = usage

    def update_session(self):
        """
        Update the session, clearing history if usage exceeds a threshold.
        """
        if self._max_usage > 0 and self._usage >= (int)(0.9 * self._max_usage):
            self._history.clear()
            if self._init_prompt is not None:
                self.add_system_message(self._init_prompt)

    @property
    def messages(self) -> List[dict]:
        """
        Get the list of messages in the session history.
        """
        return [record.message for record in self._history]

    @property
    def history(self) -> List[ChatRecord]:
        """
        Get the chat history records.
        """
        return self._history

    @abstractmethod
    def add_system_message(self, content: str):
        """
        Add a system-generated message to the session.

        :param content: The content of the system message.
        """
        pass

    @abstractmethod
    def add_user_message(self, content: str, wav_bytes: bytes):
        """
        Add a user-generated message to the session.

        :param content: The content of the user message.
        :param wav_bytes: Optional audio data associated with the message.
        """
        pass

    @abstractmethod
    def add_assistant_message(self, content: str):
        """
        Add an assistant-generated message to the session.

        :param content: The content of the assistant message.
        """
        pass

    @abstractmethod
    def add_tool_message(
        self,
        tool_name: str,
        content: str,
        tool_call_id: str = None
    ):
        """
        Add a tool-related message to the session.

        :param tool_name: The name of the tool.
        :param content: The content of the tool message.
        :param tool_call_id: Optional identifier for the tool call.
        """
        pass
