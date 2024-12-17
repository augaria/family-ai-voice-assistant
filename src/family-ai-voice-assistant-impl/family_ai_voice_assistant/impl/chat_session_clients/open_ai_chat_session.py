from family_ai_voice_assistant.core.clients import ChatSessionClient


class OpenAIChatSession(ChatSessionClient):

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
        tool_call_id: str,
        content: str
    ):
        message = {
            "role": "tool",
            "name": tool_name,
            "content": content,
            "tool_call_id": tool_call_id
        }
        self.add_message(message, True)
