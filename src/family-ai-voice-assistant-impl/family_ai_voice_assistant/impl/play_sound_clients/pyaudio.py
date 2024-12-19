import pyaudio
import wave
import time

from family_ai_voice_assistant.core.clients import PlaySoundClient


class PyAudio(PlaySoundClient):

    def __init__(self):
        super().__init__()

    def play(self, audio_file: str):
        ding_wav = wave.open(audio_file, 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        audio.terminate()
