from family_ai_voice_assistant.core.clients import VoiceWaker
from family_ai_voice_assistant.core.configs import ConfigManager
from family_ai_voice_assistant.core.helpers.common_helpers import (
    get_absolute_path_based_on_reference_file
)

from ...configs import SnowboyConfig
from ._snowboy.snowboydecoder import HotwordDetector


class SnowboyWaker(VoiceWaker):

    def __init__(self):

        config = ConfigManager().get_instance(SnowboyConfig)
        if config is None:
            raise ValueError("SnowboyConfig is not set.")
        if config.model_path is None or config.model_path == "":
            config.model_path = get_absolute_path_based_on_reference_file(
                __file__,
                "../../resources/snowboy/models/snowboy.umdl"
            )
        self._detector = HotwordDetector(config.model_path, sensitivity=0.5)

    def wake(self):
        self.start_waiting()
        self._detector.start(
            detected_callback=self._detected_callback,
            interrupt_check=lambda: not self.is_waiting(),
            sleep_time=0.03
        )
        self._detector.terminate()
        self.stop_waiting()

    def _detected_callback(self):
        self.stop_waiting()

    def check(self) -> bool:
        pass
