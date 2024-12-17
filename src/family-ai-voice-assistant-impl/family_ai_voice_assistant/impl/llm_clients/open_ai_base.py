from typing import Tuple, Dict, Any
import json

from openai.types.chat.chat_completion import ChatCompletion

from family_ai_voice_assistant.core.clients import LLMClient, ChatSessionClient
from family_ai_voice_assistant.core.contracts import FunctionInfo
from family_ai_voice_assistant.core.tools_engine import ToolFunctionsManager

from ..chat_session_clients.open_ai_chat_session import (
    OpenAIChatSession
)


class OpenAIBase(LLMClient):

    def __init__(self):
        function_infos = ToolFunctionsManager().get_function_infos(
            selected_from_config=True
        )
        self._tools_meta = [
            self._function_info_to_openai_function_meta(function_info)
            for function_info in function_infos
        ]

        super().__init__()

    def _create_session(self) -> ChatSessionClient:
        return OpenAIChatSession()

    @staticmethod
    def _function_info_to_openai_function_meta(
        function_info: FunctionInfo
    ) -> Dict:
        properties = {}
        required = []

        for param in function_info.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description
            }
            if param.is_required:
                required.append(param.name)

        return {
            "type": "function",
            "function": {
                "name": function_info.name,
                "description": function_info.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

    def _is_tool_calls_needed(self, response: Any) -> bool:
        if (
            not isinstance(response, ChatCompletion)
            or len(response.choices) == 0
        ):
            return False
        return response.choices[0].finish_reason == "tool_calls"

    def _handle_tool_calls(self, response: Any) -> None:
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
                print(result)
            self._session.add_tool_message(
                function_name, tool_call.id, json.dumps(result)
            )

    def _parse_response(self, response: Any) -> Tuple[str, int]:
        if (
            not isinstance(response, ChatCompletion)
            or len(response.choices) == 0
        ):
            return None
        return response.choices[0].message.content, response.usage.total_tokens
