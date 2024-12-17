from playsound import playsound

from family_ai_voice_assistant.core.clients import PlaySoundClient


class PlaySound(PlaySoundClient):

    def __init__(self):
        super().__init__()

    def play(self, audio_file: str):
        playsound(audio_file, True)
