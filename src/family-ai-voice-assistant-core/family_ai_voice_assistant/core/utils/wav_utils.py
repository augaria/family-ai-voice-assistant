import tempfile
from typing import Tuple

from scipy.io import wavfile
from numpy import ndarray


class WavUtils:

    @staticmethod
    def read_wav_file_to_ndarray(file_path: str) -> Tuple[int, ndarray]:
        return wavfile.read(file_path)

    @staticmethod
    def write_wav_file_from_ndarray(data: ndarray, sample_rate: int) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:  # noqa: E501
            wavfile.write(tmp_file.name, sample_rate, data)
            return tmp_file.name

    @staticmethod
    def write_wav_file_from_bytes(wav_bytes: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:  # noqa: E501
            tmp_file.write(wav_bytes)
            return tmp_file.name
