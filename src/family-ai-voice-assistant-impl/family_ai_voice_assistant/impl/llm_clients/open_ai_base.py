from typing import Tuple, Dict
import json

from openai.types.chat.chat_completion import ChatCompletion

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


class OpenAIBase(LLMClient):

    def __init__(self):
        function_infos = ToolFunctionsManager().get_function_infos(
            selected_from_config=True
        )
        self._tools_meta = [
            self._function_info_to_function_meta(function_info)
            for function_info in function_infos
        ]

        super().__init__()

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

    def _create_session(self) -> ChatSessionClient:
        return OpenAIStyleChatSession()

    def _is_tool_calls_needed(self, response: ChatCompletion) -> bool:
        if (
            not isinstance(response, ChatCompletion)
            or len(response.choices) == 0
        ):
            return False
        return response.choices[0].finish_reason == "tool_calls"

    def _handle_tool_calls(self, response: ChatCompletion) -> None:
        if (
            not isinstance(response, ChatCompletion)
            or len(response.choices) == 0
        ):
            return None

        message = response.choices[0].message
        self._session.add_message(message)

        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            try:
                result = ToolFunctionsManager().invoke_tool_function(
                    function_name,
                    function_args
                )
            except Exception as e:
                result = str(e)
                Loggers().llm.error(result)
            self._session.add_tool_message(
                function_name, json.dumps(result), tool_call.id
            )

    def _parse_response(self, response: ChatCompletion) -> Tuple[str, int]:
        if (
            not isinstance(response, ChatCompletion)
            or len(response.choices) == 0
        ):
            return None
        return response.choices[0].message.content, response.usage.total_tokens
