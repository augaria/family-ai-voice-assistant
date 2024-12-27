import sounddevice as sd
from threading import Thread, Event

from scipy.io import wavfile

from family_ai_voice_assistant.core.clients import PlaySoundClient
from family_ai_voice_assistant.core.contracts import TaskStatus
from family_ai_voice_assistant.core.clients import WaitableResultClient
from family_ai_voice_assistant.core.logging import Loggers


class SoundDeviceWaitableResult(WaitableResultClient):
    def __init__(self, event: Event):
        self._event = event
        self._status = TaskStatus.FAILED

    def set_status(self, status: TaskStatus):
        self._status = status
        self._event.set()

    def wait(self) -> TaskStatus:
        self._event.wait()
        return self._status


class SoundDevice(PlaySoundClient):
    def __init__(self):
        self._play_thread = None
        self._stop_event = Event()

    def play_async(self, audio_file: str) -> WaitableResultClient:
        Loggers().play_sound.warning(
            f"Sound Device playing audio: {audio_file}"
        )
        self._stop_event.clear()
        result = SoundDeviceWaitableResult(self._stop_event)

        def play_audio():
            try:
                sample_rate, data = wavfile.read(audio_file)
                sd.play(data, sample_rate)
                sd.wait()
                if not self._stop_event.is_set():
                    result.set_status(TaskStatus.COMPLETED)
            except Exception as e:
                Loggers().play_sound.error(f"Error playing audio: {e}")
                result.set_status(TaskStatus.FAILED)

        self._play_thread = Thread(target=play_audio)
        self._play_thread.start()
        return result

    def stop_async(self) -> WaitableResultClient:
        Loggers().play_sound.warning(
            "Sound Device stopping audio"
        )
        result = SoundDeviceWaitableResult(self._stop_event)

        def stop_audio():
            try:
                sd.stop()
                self._stop_event.set()
                result.set_status(TaskStatus.CANCELLED)
            except Exception as e:
                Loggers().play_sound.error(f"Error stopping audio: {e}")
                result.set_status(TaskStatus.FAILED)

        stop_thread = Thread(target=stop_audio)
        stop_thread.start()
        return result
