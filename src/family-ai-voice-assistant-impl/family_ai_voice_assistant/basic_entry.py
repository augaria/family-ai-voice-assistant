import argparse

from family_ai_voice_assistant.core import set_yaml_config_path
from family_ai_voice_assistant.core.client_register import (
    ClientRegistor,
    ClientSelector
)

parser = argparse.ArgumentParser(description="Start the Family AI Assistant.")
parser.add_argument('config', type=str, help='the config file path')
args = parser.parse_args()

# should be called before importing any other modules
# to make all configs available
set_yaml_config_path(args.config)


def map_configs_to_clients():

    try:
        from .impl.text_to_speech.play_sound_clients.sound_device import SoundDevice  # noqa: E501
        ClientSelector().map_play_sound_config(None, SoundDevice)
    except ImportError:
        pass

    try:
        from .impl.configs import SnowboyConfig
        from .impl.speech_to_text.waker_clients.snowboy_waker import SnowboyWaker  # noqa: E501
        ClientSelector().map_voice_waker_config(SnowboyConfig, SnowboyWaker)
    except ImportError:
        pass

    try:
        from .impl.configs import PicovoiceConfig
        from .impl.speech_to_text.waker_clients.picovoice_waker import PicovoiceWaker  # noqa: E501
        ClientSelector().map_voice_waker_config(PicovoiceConfig, PicovoiceWaker)  # noqa: E501
    except ImportError:
        pass

    try:
        from .impl.configs import AzureSpeechConfig
        from .impl.speech_to_text.recognition_clients.azure_recognition import AzureRecognition  # noqa: E501
        ClientSelector().map_recognition_config(AzureSpeechConfig, AzureRecognition)  # noqa: E501
    except ImportError:
        pass

    try:
        from .impl.configs import OpenAIWhisperConfig
        from .impl.speech_to_text.recognition_clients.openai_whisper import OpenAIWhisper  # noqa: E501
        ClientSelector().map_recognition_config(OpenAIWhisperConfig, OpenAIWhisper)  # noqa: E501
    except ImportError:
        pass

    try:
        from .impl.configs import OllamaConfig
        from .impl.llm_clients.ollama import Ollama
        ClientSelector().map_llm_config(OllamaConfig, Ollama)
    except ImportError:
        pass

    try:
        from .impl.configs import AzureOpenAIConfig
        from .impl.llm_clients.azure_open_ai import AzureOpenAI
        ClientSelector().map_llm_config(AzureOpenAIConfig, AzureOpenAI)
    except ImportError:
        pass

    try:
        from .impl.configs import OpenAIConfig
        from .impl.llm_clients.open_ai import OpenAI
        ClientSelector().map_llm_config(OpenAIConfig, OpenAI)
    except ImportError:
        pass

    try:
        from .impl.configs import AzureSpeechConfig
        from .impl.text_to_speech.speech_clients.azure_speech import AzureSpeech  # noqa: E501
        ClientSelector().map_speech_config(AzureSpeechConfig, AzureSpeech)
    except ImportError:
        pass

    try:
        from .impl.configs import CoquiTTSConfig
        from .impl.text_to_speech.speech_clients.coqui_tts import CoquiTTS
        ClientSelector().map_speech_config(CoquiTTSConfig, CoquiTTS)
    except ImportError:
        pass


def main():
    map_configs_to_clients()
    ClientRegistor().register_clients_from_selector()
    assistant = ClientRegistor().get_assistant()
    assistant.run()
