from abc import ABC, abstractmethod
from select import select


class WakerClient(ABC):
    """
    Abstract base class for a client that handles waking functionality.
    """

    __is_waiting = False

    def wake(self):
        """
        Wake the system.
        """

        self.start_waiting()

        while self.is_waiting() and (not self.check()):
            pass

        self.stop_waiting()

    @abstractmethod
    def check(self) -> bool:
        """
        Check if the wake condition is met.

        :return: True if the condition is met, otherwise False.
        """
        pass

    @abstractmethod
    def is_used_for_interrupting_ai_speaking(self) -> bool:
        """
        Determine if the waker is used for interrupting AI speaking.

        :return: True if used for interrupting, otherwise False.
        """
        pass

    @staticmethod
    def start_waiting():
        """
        Start the waiting process.
        """
        WakerClient.__is_waiting = True

    @staticmethod
    def stop_waiting():
        """
        Stop the waiting process.
        """
        WakerClient.__is_waiting = False

    @staticmethod
    def is_waiting():
        """
        Check if the system is currently waiting.

        :return: True if waiting, otherwise False.
        """
        return WakerClient.__is_waiting


class SilentWaker(WakerClient):

    def is_used_for_interrupting_ai_speaking(self) -> bool:
        return True


class VoiceWaker(WakerClient):

    def is_used_for_interrupting_ai_speaking(self) -> bool:
        return False


class KeyboardWaker(SilentWaker):

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


class InteractiveKeyboardWaker(WakerClient):

    def __init__(self):
        pass

    def check(self) -> bool:
        input("press enter to ask a question...")
        return True

    def is_used_for_interrupting_ai_speaking(self) -> bool:
        return False
