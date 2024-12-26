import platform

from family_ai_voice_assistant.core.clients import (
    WakerClient,
    GreetingClient,
    ListeningClient,
    RecognitionClient,
    LLMClient,
    SpeechClient,
    HistoryStoreClient,
    FileStoreClient,
    PlaySoundClient
)
from family_ai_voice_assistant.core.config import (
    ConfigManager,
    GeneralConfig,
    SpeechRecognitionConfig,
    FileStoreConfig,
    HistoryStoreConfig,
    KeyboardConfig
)

from family_ai_voice_assistant.core.utils.singleton_meta import SingletonMeta

from ..config import (
    PicovoiceConfig,
    SnowboyConfig,
    OpenAIWhisperConfig,
    AzureSpeechConfig,
    OpenAIConfig,
    AzureOpenAIConfig,
    OllamaConfig,
    CoquiTTSConfig
)


class ClientSelector(metaclass=SingletonMeta):

    @property
    def silent_waker(self) -> WakerClient:
        if platform.system().lower() == "linux":
            keyboard_config = ConfigManager().get_instance(
                KeyboardConfig
            )
            if keyboard_config is not None:
                from family_ai_voice_assistant.core.clients.waker_client import (  # noqa: E501
                    KeyboardWaker
                )
                return KeyboardWaker()
        return None

    @property
    def voice_waker(self) -> WakerClient:
        picovoice_config = ConfigManager().get_instance(PicovoiceConfig)
        if picovoice_config is not None:
            from ..speech_to_text.waker_clients.picovoice_waker import (
                PicovoiceWaker
            )
            return PicovoiceWaker()

        snowboy_config = ConfigManager().get_instance(SnowboyConfig)
        if snowboy_config is not None:
            from ..speech_to_text.waker_clients.snowboy_waker import (
                SnowboyWaker
            )
            return SnowboyWaker()
        return None

    @property
    def default_waker(self) -> WakerClient:
        from family_ai_voice_assistant.core.clients.waker_client import (
            InteractiveKeyboardWaker
        )
        return InteractiveKeyboardWaker()

    @property
    def greeting(self) -> GreetingClient:
        greeting_words_path = ConfigManager().get_instance(
            GeneralConfig
        ).greeting_words_path
        if greeting_words_path is not None:
            from family_ai_voice_assistant.core.clients.greeting_client import (  # noqa: E501
                RandomGreetingWordsFromList
            )
            return RandomGreetingWordsFromList()
        return None

    @property
    def listening(self) -> ListeningClient:
        speech_recognition_config = ConfigManager().get_instance(
            SpeechRecognitionConfig
        )
        if speech_recognition_config is not None:
            from family_ai_voice_assistant.core.clients.listening_client import (  # noqa: E501
                SpeechRecognitionListening
            )
            return SpeechRecognitionListening()
        raise NotImplementedError("Listening config not provided")

    @property
    def recognition(self) -> RecognitionClient:
        azure_speech_config = ConfigManager().get_instance(AzureSpeechConfig)
        if azure_speech_config is not None:
            from ..speech_to_text.recognition_clients.azure_recognition import (  # noqa: E501
                AzureRecognition
            )
            return AzureRecognition()

        open_ai_whisper_config = ConfigManager().get_instance(
            OpenAIWhisperConfig
        )
        if open_ai_whisper_config is not None:
            from ..speech_to_text.recognition_clients.openai_whisper import (
                OpenAIWhisper
            )
            return OpenAIWhisper()

        raise NotImplementedError("Recognition config not provided")

    @property
    def llm(self) -> LLMClient:
        ollama_config = ConfigManager().get_instance(OllamaConfig)
        if ollama_config is not None:
            from ..llm_clients.ollama import Ollama
            return Ollama()

        open_ai_config = ConfigManager().get_instance(OpenAIConfig)
        if open_ai_config is not None:
            from ..llm_clients.open_ai import OpenAI
            return OpenAI()

        azure_open_ai_config = ConfigManager().get_instance(AzureOpenAIConfig)
        if azure_open_ai_config is not None:
            from ..llm_clients.azure_open_ai import AzureOpenAI
            return AzureOpenAI()

        raise NotImplementedError("LLM config not provided")

    @property
    def speech(self) -> SpeechClient:
        azure_speech_config = ConfigManager().get_instance(AzureSpeechConfig)
        if azure_speech_config is not None:
            from ..text_to_speech.speech_clients.azure_speech import (
                AzureSpeech
            )
            return AzureSpeech()

        coqui_tts_config = ConfigManager().get_instance(CoquiTTSConfig)
        if coqui_tts_config is not None:
            from ..text_to_speech.speech_clients.coqui_tts import (
                CoquiTTS
            )
            return CoquiTTS()

        raise NotImplementedError("Speech config not provided")

    @property
    def history_store(self) -> HistoryStoreClient:
        history_store_config = ConfigManager().get_instance(HistoryStoreConfig)
        if (
            history_store_config is None
            or history_store_config.connection_str is None
        ):
            return None

        if history_store_config.connection_str.startswith("mongodb:"):
            from family_ai_voice_assistant.core.clients.history_store_client import (  # noqa: E501
                MongoHistoryStore
            )
            return MongoHistoryStore()
        else:
            raise NotImplementedError(
                "History store not implemented for connection string: "
                f"{history_store_config.connection_str}"
            )

    @property
    def file_store(self) -> FileStoreClient:
        file_store_config = ConfigManager().get_instance(FileStoreConfig)
        if file_store_config is None or file_store_config.destination is None:
            return None
        if file_store_config.destination.startswith("http"):
            from family_ai_voice_assistant.core.clients.file_store_client import (  # noqa: E501
                RestFileStore
            )
            return RestFileStore()
        else:
            from family_ai_voice_assistant.core.clients.file_store_client import (  # noqa: E501
                LocalFileStore
            )
            return LocalFileStore()

    @property
    def play_sound(self) -> PlaySoundClient:
        try:
            from ..text_to_speech.play_sound_clients.sound_device import (
                SoundDevice
            )
            return SoundDevice()
        except ImportError:
            return None
