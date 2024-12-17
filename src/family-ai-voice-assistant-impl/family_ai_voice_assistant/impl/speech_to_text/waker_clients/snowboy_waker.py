from family_ai_voice_assistant.core.clients import WakerClient
from family_ai_voice_assistant.core.config import ConfigManager
from family_ai_voice_assistant.core.utils.common_utils import (
    get_absolute_path_based_on_reference_file
)

from ...config import SnowboyConfig
from ._snowboy.snowboydecoder import HotwordDetector


class SnowboyWaker(WakerClient):

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
        self.interrupted = False

    def wake(self):
        WakerClient.is_waiting = True
        self.interrupted = False
        self._detector.start(
            detected_callback=self._detected_callback,
            interrupt_check=lambda: self.interrupted,
            sleep_time=0.03
        )
        print("[detector start ended]")
        self._detector.terminate()
        print("[detector terminated]")
        WakerClient.is_waiting = False

    def _detected_callback(self):
        print("Wake word detected!")
        self.interrupted = True

    def check(self) -> bool:
        pass

    def is_used_for_interrupting_ai_speeking() -> bool:
        return False