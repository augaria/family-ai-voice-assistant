from typing import Any

from openai import OpenAI as OpenAIClient
from family_ai_voice_assistant.core.configs import ConfigManager

from .open_ai_base import OpenAIBase
from ..configs import OpenAIConfig


class OpenAI(OpenAIBase):

    def __init__(self):

        self._config = ConfigManager().get_instance(OpenAIConfig)
        if self._config is None:
            raise ValueError("OpenAIConfig is not set.")

        if self._config.api_base is not None and self._config.api_base != "":
            base_url = self._config.api_base
        else:
            base_url = None
        self._client = OpenAIClient(
            base_url=base_url,
            api_key=self._config.api_key
        )

        super().__init__()

    def _chat(self) -> Any:
        return self._client.chat.completions.create(
            messages=self._session.messages,
            model=self._config.model,
            tool_choice='auto',
            tools=self._tools_meta
        )
