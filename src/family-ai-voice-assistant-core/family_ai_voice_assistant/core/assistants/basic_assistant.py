import os
import asyncio
import concurrent.futures
import threading
from typing import Tuple

from ..contracts import TaskStatus
from ..clients import (
    AssistantClient,
    ClientManager,
    WakerClient,
    GreetingClient,
    ListeningClient,
    RecognitionClient,
    LLMClient,
    SpeechClient,
    PlaySoundClient
)
from ..helpers.constants_provider import ConstantsProvider
from ..utils.program_control import ProgramControl
from ..utils.ai_output_filter import AiOutputFilter
from ..telemetry import trace
from ..logging import Loggers, colored_print, Fore
from ..configs import ConfigManager, GeneralConfig


class BasicAssistant(AssistantClient):

    def __init__(self):
        self._wakers = ClientManager().get_all_clients(WakerClient)
        self._greeting_client = ClientManager().get_client(GreetingClient)
        self._listening_client = ClientManager().get_client(ListeningClient)
        self._recognition_client = ClientManager().get_client(
            RecognitionClient
        )
        self._llm_client = ClientManager().get_client(LLMClient)
        self._speech_client = ClientManager().get_client(SpeechClient)
        self._play_sound_client = ClientManager().get_client(PlaySoundClient)

        if not self._listening_client:
            raise Exception(
                "Listening client should be provided to ClientManager"
            )
        if not self._speech_client:
            raise Exception(
                "Speech client should be provided to ClientManager"
            )
        if not self._llm_client:
            raise Exception("LLM client should be provided to ClientManager")
        if not self._recognition_client:
            raise Exception(
                "Recognition client should be provided to ClientManager"
            )
        if len(self._wakers) == 0:
            raise Exception(
                "At least one waker client should be provided to ClientManager"
            )

        self._speech_status_lock = threading.Lock()
        self._speech_finished = False

        general_config = ConfigManager().get_instance(GeneralConfig)
        self._bot_name = general_config.bot_name
        self._user_name = general_config.user_name

    def run(self):

        Loggers().assistant.info("[started]")

        service_start_message = ConstantsProvider().get(
            'SERVICE_START_MESSAGE'
        ).format(
            bot_name=self._bot_name
        )

        self._speech_client.speech(service_start_message)

        while not ProgramControl().is_exit:
            try:
                Loggers().assistant.info("[AI Waiting]")
                self.wake()
                Loggers().assistant.info("[AI Waked]")

                self.serve()
            except Exception as e:
                Loggers().assistant.info(e)
                bot_error_message = ConstantsProvider().get(
                    'BOT_ERROR_MESSAGE'
                )
                self._speech_client.speech(bot_error_message)

        self._llm_client.end_session()

    @trace()
    def serve(self):
        if self._greeting_client:
            greeting_words = self._greeting_client.words()
        else:
            greeting_words = ConstantsProvider().get(
                'BOT_HELLO_MESSAGE'
            )

        Loggers().assistant.info("[AI greeting]")
        self._speech_client.speech(greeting_words)

        Loggers().assistant.info("[AI Listening]")
        question, wav_bytes = asyncio.run(
            self.speech_to_wav_and_text()
        )
        if (not question) or (question == ""):
            bot_rest_message = ConstantsProvider().get(
                'BOT_REST_MESSAGE'
            )
            self._speech_client.speech(bot_rest_message)
            return
        self.answer(
            question=question,
            speak_answer=True,
            enable_interrupt=True,
            wav_bytes=wav_bytes
        )

    @trace()
    def answer(
        self,
        question: str,
        speak_answer: bool = True,
        enable_interrupt: bool = True,
        wav_bytes: bytes = None
    ) -> str:
        colored_print(f"[{self._user_name}] {question}", Fore.CYAN)
        Loggers().assistant.info("[AI thinking]")
        ans = self._llm_client.chat(question, wav_bytes)
        colored_print(f"[{self._bot_name}] {ans}", Fore.MAGENTA)
        if speak_answer:
            Loggers().assistant.info("[AI speaking]")
            self.text_to_speech(
                text=AiOutputFilter.filter_output(ans),
                enable_interrupt=enable_interrupt
            )
            Loggers().assistant.info("[AI finished]")
        return ans

    def wake(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [executor.submit(waker.wake) for waker in self._wakers]
            concurrent.futures.wait(
                tasks, return_when=concurrent.futures.ALL_COMPLETED
            )

    async def speech_to_wav_and_text(self) -> Tuple[str, bytes]:
        audio = self._listening_client.listen()
        if audio is None:
            return None
        Loggers().assistant.info("[Caught user's voice]")

        if self._play_sound_client:
            notice_sound_file = os.path.join(
                os.path.dirname(__file__),
                '../resources/ding.wav'
            )
            self._play_sound_client.play(notice_sound_file)

        Loggers().assistant.info("[Transfering voice to text]")
        text = self._recognition_client.recognize(audio)
        wav_bytes = self._listening_client.get_wav_from_audio(audio)
        return text, wav_bytes

    def text_to_speech(self, text: str, enable_interrupt: bool = True):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            speech_task = executor.submit(
                self._speech_and_stop_wait,
                text,
                enable_interrupt
            )
            tasks = [speech_task]
            if enable_interrupt:
                interrupt_task = executor.submit(
                    self._wait_and_interrupt_speech
                )
                tasks.append(interrupt_task)
            concurrent.futures.wait(
                tasks, return_when=concurrent.futures.ALL_COMPLETED
            )

    def _speech_and_stop_wait(self, text: str, enable_interrupt: bool = True):
        with self._speech_status_lock:
            self._speech_finished = False
        res = self._speech_client.speech(text)
        if res != TaskStatus.COMPLETED:
            Loggers().assistant.warning(f"text-to-speech failed: {res}")
        with self._speech_status_lock:
            self._speech_finished = True
        if enable_interrupt:
            WakerClient.stop_waiting()

    def _wait_and_interrupt_speech(self):
        interrupt = self._wait_for_interrupt_signal()
        if not interrupt:
            return
        with self._speech_status_lock:
            if not self._speech_finished:
                self._speech_client.stop()

    def _wait_for_interrupt_signal(self) -> bool:
        interrupting_wakers = [
            waker for waker in self._wakers
            if waker.is_used_for_interrupting_ai_speaking()
        ]
        if len(interrupting_wakers) == 0:
            return False
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [
                executor.submit(waker.wake) for waker in interrupting_wakers
            ]
            concurrent.futures.wait(
                tasks, return_when=concurrent.futures.ALL_COMPLETED
            )
            return True
