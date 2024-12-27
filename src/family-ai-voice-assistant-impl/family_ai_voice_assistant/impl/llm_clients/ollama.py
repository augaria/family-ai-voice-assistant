from typing import Tuple, Dict
import json

from ollama import Client
from ollama import ChatResponse

from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.clients import LLMClient, ChatSessionClient
from family_ai_voice_assistant.core.contracts import (
    FunctionInfo,
    LLMFunctionDefBase
)
from family_ai_voice_assistant.core.tools_engine import ToolFunctionsManager
from family_ai_voice_assistant.core.logging import Loggers

from ..chat_session_clients.open_ai_style_chat_session import (
    OpenAIStyleChatSession
)
from ..configs import OllamaConfig


class Ollama(LLMClient):

    def __init__(self):
        self._config = ConfigManager().get_instance(OllamaConfig)
        if self._config is None:
            raise ValueError("OllamaConfig is not set.")

        self._client = Client(
            host=self._config.host
        )

        function_infos = ToolFunctionsManager().get_function_infos(
            selected_from_config=True
        )
        self._tools_meta = [
            self._function_info_to_function_meta(function_info)
            for function_info in function_infos
        ]

        super().__init__()

    def _create_session(self) -> ChatSessionClient:
        return OpenAIStyleChatSession()

    @staticmethod
    def _function_info_to_function_meta(
        function_info: FunctionInfo
    ) -> Dict:
        return {
            "type": "function",
            "function": (
                LLMFunctionDefBase.from_function_info(function_info).to_dict()
            )
        }

    def _is_tool_calls_needed(self, response: ChatResponse) -> bool:
        if not isinstance(response, ChatResponse):
            return False
        return response.message.tool_calls is not None

    def _handle_tool_calls(self, response: ChatResponse) -> None:
        if not isinstance(response, ChatResponse):
            return None

        message = response.message
        self._session.add_message(message)

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = tool_call.function.arguments
            try:
                result = ToolFunctionsManager().invoke_tool_function(
                    function_name,
                    function_args
                )
            except Exception as e:
                result = str(e)
                Loggers().llm.error(result)
            self._session.add_tool_message(
                function_name, None, json.dumps(result)
            )

    def _parse_response(self, response: ChatResponse) -> Tuple[str, int]:
        if not isinstance(response, ChatResponse):
            return None
        return response.message.content, 0

    def _chat(self) -> ChatResponse:
        return self._client.chat(
            model=self._config.model,
            messages=self._session.messages,
            tools=self._tools_meta
        )
