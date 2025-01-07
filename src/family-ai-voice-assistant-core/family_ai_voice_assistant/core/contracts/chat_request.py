from dataclasses import dataclass

from .dict_convertible import DictConvertible


@dataclass
class ChatRequest(DictConvertible):
    """
    A data class representing the schema for the body of a chat API request.

    Attributes:
        question (str): The question to be processed by the API.
        speak_answer (bool): Indicates whether the answer should be played through a speaker.  # noqa: E501
    """
    question: str
    speak_answer: bool
