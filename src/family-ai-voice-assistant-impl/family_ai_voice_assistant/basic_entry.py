import argparse

from family_ai_voice_assistant.core import set_yaml_config_path

parser = argparse.ArgumentParser(description="Start the Family AI Assistant.")
parser.add_argument('config', type=str, help='the config file path')
args = parser.parse_args()

# should be called before importing any other modules
# to make all configs available
set_yaml_config_path(args.config)

from family_ai_voice_assistant.core.clients import (  # noqa: E402
    ClientManager,
    WakerClient,
    GreetingClient,
    ListeningClient,
    RecognitionClient,
    LLMClient,
    SpeechClient,
    FileStoreClient,
    HistoryStoreClient,
    PlaySoundClient
)
from family_ai_voice_assistant.core.family_ai_voice_assistant import (  # noqa: E402, E501
    FamilyAIAssistant
)

from .impl.utils.client_selector import ClientSelector  # noqa: E402


def register_clients():

    silent_waker = ClientSelector().silent_waker
    if silent_waker:
        ClientManager().register_client(
            WakerClient,
            ClientSelector().silent_waker
        )
    voice_waker = ClientSelector().voice_waker
    if voice_waker:
        ClientManager().register_client(
            WakerClient,
            voice_waker
        )
    if not silent_waker and not voice_waker:
        raise Exception("At least one waker should be provided.")

    ClientManager().register_client(
        GreetingClient,
        ClientSelector().greeting
    )

    ClientManager().register_client(
        ListeningClient,
        ClientSelector().listening
    )

    ClientManager().register_client(
        RecognitionClient,
        ClientSelector().recognition
    )

    ClientManager().register_client(
        LLMClient,
        ClientSelector().llm
    )

    ClientManager().register_client(
        SpeechClient,
        ClientSelector().speech
    )

    file_store = ClientSelector().file_store
    if file_store:
        ClientManager().register_client(
            FileStoreClient,
            file_store
        )

    history_store = ClientSelector().history_store
    if history_store:
        ClientManager().register_client(
            HistoryStoreClient,
            history_store
        )

    play_sound = ClientSelector().play_sound
    if play_sound:
        ClientManager().register_client(
            PlaySoundClient,
            play_sound
        )


def main():
    register_clients()
    assistant = FamilyAIAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
