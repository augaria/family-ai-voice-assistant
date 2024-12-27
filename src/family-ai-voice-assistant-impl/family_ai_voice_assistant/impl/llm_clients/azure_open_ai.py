from typing import Any

from openai import AzureOpenAI as AzureOpenAIClient
from family_ai_voice_assistant.core.configs import ConfigManager

from .open_ai_base import OpenAIBase
from ..configs import AzureOpenAIConfig


class AzureOpenAI(OpenAIBase):

    def __init__(self):

        self._config = ConfigManager().get_instance(AzureOpenAIConfig)
        if self._config is None:
            raise ValueError("AzureOpenAIConfig is not set.")

        self._client = AzureOpenAIClient(
            api_key=self._config.api_key,
            api_version=self._config.api_version,
            azure_endpoint=self._config.api_base,
            azure_deployment=self._config.deployment_name
        )

        super().__init__()

    def _chat(self) -> Any:
        return self._client.chat.completions.create(
            messages=self._session.messages,
            model=self._config.deployment_name,
            tool_choice='auto',
            tools=self._tools_meta
        )
