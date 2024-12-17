from abc import ABC, abstractmethod
from typing import Tuple, Any
from threading import Timer

from opentelemetry import trace as otl_trace

from .chat_session_client import ChatSessionClient
from .history_store_client import HistoryStoreClient
from .client_manager import ClientManager
from ..config import ConfigManager, ChatSessionConfig
from ..utils.constants_provider import ConstantsProvider
from ..utils.language_manager import LanguageManager
from ..telemetry import trace
from ..logging import Loggers


class LLMClient(ABC):

    def __init__(self):
        self._session: ChatSessionClient = None
        self._timer: Timer = None

    @trace()
    def chat(self, question: str, wav_bytes: bytes) -> str:
        try:
            if self._session is None:
                self._session = self._create_session()
            self._session.add_user_message(question, wav_bytes)
            ans, token_usage = self._call_llm()

            span = otl_trace.get_current_span()
            span.set_attribute('token_usage', token_usage)

            self._session.add_assistant_message(ans)
            self._session.set_usage(token_usage)
            self._session.update_session()
            self._reset_session_timer()
            return ans

        except Exception as e:
            self._on_session_expired()
            print(e)
            session_error_message = ConstantsProvider().get(
                'SESSION_ERROR_MESSAGE'
            )
            return session_error_message

    def end_session(self):
        self._cancel_timer()
        self._on_session_expired()

    def _call_llm(self) -> Tuple[str, int]:
        response = self._chat()
        if self._is_tool_calls_needed(response):
            self._handle_tool_calls(response)
            response = self._chat()
        return self._parse_response(response)

    def _on_session_expired(self):
        try:
            history_store_client = ClientManager().get_client(
                HistoryStoreClient
            )
            if (
                history_store_client is not None
                and self._session is not None
                and len(self._session.history) > 0
            ):
                history_store_client.save(self._session.history)
        except Exception as e:
            Loggers().llm.error(
                f"Failed to save session history: {str(e)}"
            )
        self._session = None
        LanguageManager().set()  # reset language to default from config

    def _cancel_timer(self):
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _reset_session_timer(self):
        self._cancel_timer()
        self._timer = Timer(
            ConfigManager().get_instance(ChatSessionConfig).session_timeout,
            self._on_session_expired
        )
        self._timer.start()

    @abstractmethod
    def _create_session(self) -> ChatSessionClient:
        pass

    @abstractmethod
    def _chat(self) -> Any:
        pass

    @abstractmethod
    def _is_tool_calls_needed(self, response: Any) -> bool:
        pass

    @abstractmethod
    def _handle_tool_calls(self, response: Any) -> None:
        pass

    @abstractmethod
    def _parse_response(self, response: Any) -> Tuple[str, int]:
        pass
