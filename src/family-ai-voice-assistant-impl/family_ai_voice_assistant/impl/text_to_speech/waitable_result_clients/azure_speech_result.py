from azure.cognitiveservices.speech import (
    SpeechRecognitionResult,
    ResultFuture,
    ResultReason,
    CancellationReason
)

from family_ai_voice_assistant.core.contracts import TaskStatus
from family_ai_voice_assistant.core.clients import WaitableResultClient
from family_ai_voice_assistant.core.logging import Loggers


class AzureSpeechResult(WaitableResultClient):

    def __init__(self, result_future: ResultFuture):
        self._result_future = result_future

    def wait(self) -> TaskStatus:
        Loggers().waitable_result.info("Waiting for speech result")
        result: SpeechRecognitionResult = self._result_future.get()
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            return TaskStatus.COMPLETED
        elif result.reason == ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            if cancellation_details.reason == CancellationReason.Error:
                return TaskStatus.FAILED
            return TaskStatus.CANCELLED
