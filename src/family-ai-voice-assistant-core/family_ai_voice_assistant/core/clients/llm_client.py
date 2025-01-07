from abc import ABC, abstractmethod
from typing import Tuple, Any
from threading import Timer

from opentelemetry import trace as otl_trace

from .chat_session_client import ChatSessionClient
from .history_store_client import HistoryStoreClient
from .client_manager import ClientManager
from ..configs import ConfigManager, ChatSessionConfig
from ..helpers.constants_provider import ConstantsProvider
from ..helpers.language_manager import LanguageManager
from ..telemetry import trace
from ..logging import Loggers


class LLMClient(ABC):
    """
    Manages interactions with a language model, handling chat sessions.
    """

    def __init__(self):
        self._session: ChatSessionClient = None
        self._timer: Timer = None

    @trace()
    def chat(self, question: str, wav_bytes: bytes) -> str:
        """
        Conduct a chat session with the language model.

        :param question: The user's question.
        :param wav_bytes: Optional audio data for the question.
        :return: The response from the language model.
        """

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
            Loggers().llm.error(e)
            session_error_message = ConstantsProvider().get(
                'SESSION_ERROR_MESSAGE'
            )
            return session_error_message

    def end_session(self):
        """
        End the current chat session.
        """
        self._cancel_timer()
        self._on_session_expired()

    def _call_llm(self) -> Tuple[str, int]:
        """
        Call the language model and handle tool calls if needed.

        :return: A tuple of the response and token usage.
        """

        response = self._chat()
        if self._is_tool_calls_needed(response):
            self._handle_tool_calls(response)
            response = self._chat()
        return self._parse_response(response)

    def _on_session_expired(self):
        """
        Handle session expiration by saving history and resetting state.
        """

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
        """
        Cancel the session timer if active.
        """
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None

    def _reset_session_timer(self):
        """
        Reset the session timer to handle session expiration.
        """
        self._cancel_timer()
        self._timer = Timer(
            ConfigManager().get_instance(ChatSessionConfig).session_timeout,
            self._on_session_expired
        )
        self._timer.start()

    @abstractmethod
    def _create_session(self) -> ChatSessionClient:
        """
        Create a new chat session.
        """
        pass

    @abstractmethod
    def _chat(self) -> Any:
        """
        Send a chat request to the language model.
        """
        pass

    @abstractmethod
    def _is_tool_calls_needed(self, response: Any) -> bool:
        """
        Determine if tool calls are needed based on the response.

        :param response: The response from the language model.
        :return: True if tool calls are needed, otherwise False.
        """
        pass

    @abstractmethod
    def _handle_tool_calls(self, response: Any) -> None:
        """
        Handle any required tool calls based on the response.

        :param response: The response from the language model.
        """
        pass

    @abstractmethod
    def _parse_response(self, response: Any) -> Tuple[str, int]:
        """
        Parse the response from the language model.

        :param response: The response to parse.
        :return: A tuple of the parsed response and token usage.
        """
        pass
