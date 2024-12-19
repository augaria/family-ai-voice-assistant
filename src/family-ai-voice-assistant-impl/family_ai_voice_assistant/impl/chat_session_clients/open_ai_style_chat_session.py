from family_ai_voice_assistant.core.clients import ChatSessionClient


class OpenAIStyleChatSession(ChatSessionClient):

    def add_system_message(self, content: str):
        message = {
            "role": "system",
            "content": content
        }
        self.add_message(message, True)

    def add_user_message(self, content: str, wav_bytes: bytes):
        message = {
            "role": "user",
            "content": content
        }
        self.add_message(message, True, wav_bytes)

    def add_assistant_message(self, content: str):
        message = {
            "role": "assistant",
            "content": content
        }
        self.add_message(message, True)

    def add_tool_message(
        self,
        tool_name: str,
        content: str,
        tool_call_id: str = None
    ):
        message = {
            "role": "tool",
            "name": tool_name,
            "content": content
        }
        if tool_call_id is not None:
            message["tool_call_id"] = tool_call_id
        self.add_message(message, True)
