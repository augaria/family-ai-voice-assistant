from .utils.singleton_meta import SingletonMeta
from .clients import (
    ClientManager,
    WakerClient,
    GreetingClient,
    ListeningClient,
    RecognitionClient,
    LLMClient,
    SpeechClient,
    FileStoreClient,
    HistoryStoreClient,
    PlaySoundClient,
    AssistantClient
)

from .client_selector import ClientSelector


class ClientRegistor(metaclass=SingletonMeta):
    """
    Registers and manages clients for various functionalities in the system.
    """

    def get_assistant(self) -> AssistantClient:
        """
        Retrieve the assistant client instance.

        :return: An instance of AssistantClient.
        """

        return ClientManager().get_client(AssistantClient)

    def register_clients_from_selector(self):
        """
        Register clients using the ClientSelector. Determines which clients to register  # noqa: E501
        based on availability and defaults to ensure all necessary components are initialized.  # noqa: E501
        """

        silent_waker = ClientSelector().get_silent_waker()
        if silent_waker:
            ClientManager().register_client(
                WakerClient,
                silent_waker
            )
        voice_waker = ClientSelector().get_voice_waker()
        if voice_waker:
            ClientManager().register_client(
                WakerClient,
                voice_waker
            )
        if not silent_waker and not voice_waker:
            ClientManager().register_client(
                WakerClient,
                ClientSelector().get_default_waker()
            )

        ClientManager().register_client(
            GreetingClient,
            ClientSelector().get_greeting()
        )

        ClientManager().register_client(
            ListeningClient,
            ClientSelector().get_listening()
        )

        ClientManager().register_client(
            RecognitionClient,
            ClientSelector().get_recognition()
        )

        ClientManager().register_client(
            LLMClient,
            ClientSelector().get_llm()
        )

        ClientManager().register_client(
            SpeechClient,
            ClientSelector().get_speech()
        )

        ClientManager().register_client(
            FileStoreClient,
            ClientSelector().get_file_store()
        )

        ClientManager().register_client(
            HistoryStoreClient,
            ClientSelector().get_history_store()
        )

        ClientManager().register_client(
            PlaySoundClient,
            ClientSelector().get_play_sound()
        )

        ClientManager().register_client(
            AssistantClient,
            ClientSelector().get_assistant()
        )
