from abc import ABC, abstractmethod
from select import select


class WakerClient(ABC):

    is_waiting = False

    def wake(self):
        WakerClient.is_waiting = True

        while WakerClient.is_waiting and (not self.check()):
            pass

        WakerClient.is_waiting = False

    @abstractmethod
    def check(self) -> bool:
        pass

    def is_used_for_interrupting_ai_speaking(self) -> bool:
        return False


class KeyboardWaker(WakerClient):

    def __init__(self):
        import platform
        if platform.system().lower() != "linux":
            raise Exception("KeyboardWaker is only supported on Linux.")
        import evdev  # type: ignore
        from ..configs import ConfigManager, KeyboardConfig
        config = ConfigManager().get_instance(KeyboardConfig)
        if config is None or config.device is None:
            raise ValueError("Keyboard device is not set.")
        self._device = evdev.InputDevice(config.device)
        self._target_key = evdev.ecodes.EV_KEY

    def check(self) -> bool:
        select([self._device], [], [], 1)
        try:
            detected = False
            for event in self._device.read():
                if event.type == self._target_key:
                    detected = True
                    break
            if detected:
                select([self._device], [], [])
                for event in self._device.read():
                    pass
                return True
        except BlockingIOError:
            return False

        return False

    def is_used_for_interrupting_ai_speaking(self) -> bool:
        return True


class InteractiveKeyboardWaker(WakerClient):

    def __init__(self):
        pass

    def check(self) -> bool:
        input("press enter to ask a question...")
        return True
