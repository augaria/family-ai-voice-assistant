from typing import Dict, List, Tuple
import platform

from .utils.singleton_meta import SingletonMeta
from .clients import (
    WakerClient,
    SilentWaker,
    VoiceWaker,
    GreetingClient,
    ListeningClient,
    RecognitionClient,
    ChatSessionClient,
    LLMClient,
    SpeechClient,
    WaitableResultClient,
    FileStoreClient,
    HistoryStoreClient,
    PlaySoundClient,
    AssistantClient
)
from .configs import (
    ConfigManager,
    GeneralConfig,
    SpeechRecognitionConfig,
    FileStoreConfig,
    HistoryStoreConfig,
    KeyboardConfig,
    AssistantApiConfig
)
from .clients.listening_client import SpeechRecognitionListening
from .assistants.assistant_with_api import AssistantWithApi


class ClientSelector(metaclass=SingletonMeta):

    def __init__(self):
        self._client_map: Dict[type, List[Tuple[type, type]]] = {
            SilentWaker: [],
            VoiceWaker: [],
            GreetingClient: [],
            ListeningClient: [],
            RecognitionClient: [],
            ChatSessionClient: [],
            LLMClient: [],
            SpeechClient: [],
            WaitableResultClient: [],
            FileStoreClient: [],
            HistoryStoreClient: [],
            PlaySoundClient: [],
            AssistantClient: []
        }

        if platform.system().lower() == "linux":
            from .clients.waker_client import KeyboardWaker
            self.map_silent_waker_config(
                KeyboardConfig,
                KeyboardWaker
            )

        self.map_listening_config(
            SpeechRecognitionConfig,
            SpeechRecognitionListening
        )

        self.map_assistant_config(
            AssistantApiConfig,
            AssistantWithApi
        )

    def map_silent_waker_config(
        self,
        config_type: type,
        client_type: type[SilentWaker]
    ):
        self._map_config_to_client(
            SilentWaker,
            config_type,
            client_type
        )

    def map_voice_waker_config(
        self,
        config_type: type,
        client_type: type[VoiceWaker]
    ):
        self._map_config_to_client(
            VoiceWaker,
            config_type,
            client_type
        )

    def map_greeting_config(
        self,
        config_type: type,
        client_type: type[GreetingClient]
    ):
        self._map_config_to_client(
            GreetingClient,
            config_type,
            client_type
        )

    def map_listening_config(
        self,
        config_type: type,
        client_type: type[ListeningClient]
    ):
        self._map_config_to_client(
            ListeningClient,
            config_type,
            client_type
        )

    def map_recognition_config(
        self,
        config_type: type,
        client_type: type[RecognitionClient]
    ):
        self._map_config_to_client(
            RecognitionClient,
            config_type,
            client_type
        )

    def map_llm_config(
        self,
        config_type: type,
        client_type: type[LLMClient]
    ):
        self._map_config_to_client(
            LLMClient,
            config_type,
            client_type
        )

    def map_speech_config(
        self,
        config_type: type,
        client_type: type[SpeechClient]
    ):
        self._map_config_to_client(
            SpeechClient,
            config_type,
            client_type
        )

    def map_waitable_result_config(
        self,
        config_type: type,
        client_type: type[WaitableResultClient]
    ):
        self._map_config_to_client(
            WaitableResultClient,
            config_type,
            client_type
        )

    def map_file_store_config(
        self,
        config_type: type,
        client_type: type[FileStoreClient]
    ):
        self._map_config_to_client(
            FileStoreClient,
            config_type,
            client_type
        )

    def map_history_store_config(
        self,
        config_type: type,
        client_type: type[HistoryStoreClient]
    ):
        self._map_config_to_client(
            HistoryStoreClient,
            config_type,
            client_type
        )

    def map_play_sound_config(
        self,
        config_type: type,
        client_type: type[PlaySoundClient]
    ):
        self._map_config_to_client(
            PlaySoundClient,
            config_type,
            client_type
        )

    def map_assistant_config(
        self,
        config_type: type,
        client_type: type[AssistantClient]
    ):
        self._map_config_to_client(
            AssistantClient,
            config_type,
            client_type
        )

    def get_silent_waker(self) -> SilentWaker:
        return self._get_client_by_config(SilentWaker)

    def get_voice_waker(self) -> VoiceWaker:
        return self._get_client_by_config(VoiceWaker)

    def get_default_waker(self) -> WakerClient:
        from .clients.waker_client import (
            InteractiveKeyboardWaker
        )
        return InteractiveKeyboardWaker()

    def get_greeting(self) -> GreetingClient:
        client = self._get_client_by_config(GreetingClient)
        if client is not None:
            return client

        greeting_words_path = ConfigManager().get_instance(
            GeneralConfig
        ).greeting_words_path
        if greeting_words_path is not None:
            from .clients.greeting_client import (  # noqa: E501
                RandomGreetingWordsFromList
            )
            return RandomGreetingWordsFromList()
        return None

    def get_listening(self) -> ListeningClient:
        client = self._get_client_by_config(ListeningClient)
        if client is not None:
            return client
        raise NotImplementedError("Listening config not provided")

    def get_recognition(self) -> RecognitionClient:
        client = self._get_client_by_config(RecognitionClient)
        if client is not None:
            return client
        raise NotImplementedError("Recognition config not provided")

    def get_llm(self) -> LLMClient:
        client = self._get_client_by_config(LLMClient)
        if client is not None:
            return client
        raise NotImplementedError("LLM config not provided")

    def get_speech(self) -> SpeechClient:
        client = self._get_client_by_config(SpeechClient)
        if client is not None:
            return client
        raise NotImplementedError("Speech config not provided")

    def get_history_store(self) -> HistoryStoreClient:
        client = self._get_client_by_config(HistoryStoreClient)
        if client is not None:
            return client

        history_store_config = ConfigManager().get_instance(HistoryStoreConfig)
        if (
            history_store_config is None
            or history_store_config.connection_str is None
        ):
            return None

        if history_store_config.connection_str.startswith("mongodb:"):
            from .clients.history_store_client import (  # noqa: E501
                MongoHistoryStore
            )
            return MongoHistoryStore()
        else:
            raise NotImplementedError(
                "History store not implemented for connection string: "
                f"{history_store_config.connection_str}"
            )

    def get_file_store(self) -> FileStoreClient:
        client = self._get_client_by_config(FileStoreClient)
        if client is not None:
            return client

        file_store_config = ConfigManager().get_instance(FileStoreConfig)
        if file_store_config is None or file_store_config.destination is None:
            return None
        if file_store_config.destination.startswith("http"):
            from .clients.file_store_client import (  # noqa: E501
                RestFileStore
            )
            return RestFileStore()
        else:
            from .clients.file_store_client import (  # noqa: E501
                LocalFileStore
            )
            return LocalFileStore()

    def get_play_sound(self) -> PlaySoundClient:
        client = self._get_client_by_config(PlaySoundClient)
        if client is not None:
            return client
        raise NotImplementedError("Play sound client not provided")

    def get_assistant(self) -> AssistantClient:
        client = self._get_client_by_config(AssistantClient)
        if client is not None:
            return client

        from .assistants.basic_assistant import (
            BasicAssistant
        )
        return BasicAssistant()

    def _map_config_to_client(
        self,
        client_base_type: type,
        client_config_type: type,
        client_type: type,
    ):
        if client_base_type not in self._client_map:
            raise ValueError(
                f"Client base type [{client_base_type}] is not supported"
            )
        if not issubclass(client_type, client_base_type):
            raise ValueError(
                f"Client type [{client_type}] "
                f"is not a subclass of [{client_base_type}]"
            )
        self._client_map[client_base_type].append(
            (client_config_type, client_type)
        )

    def _get_client_by_config(self, client_base_type: type):
        if client_base_type not in self._client_map:
            raise ValueError(
                f"Client base type [{client_base_type}] is not supported"
            )
        for client_config_type, client_type in self._client_map[client_base_type]:  # noqa: E501
            if client_config_type is None:
                return client_type()
            config = ConfigManager().get_instance(client_config_type)
            if config is not None:
                return client_type()
        return None
