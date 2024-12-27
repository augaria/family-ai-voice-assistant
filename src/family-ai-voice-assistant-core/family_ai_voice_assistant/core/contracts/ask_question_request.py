from dataclasses import dataclass

from .dict_convertible import DictConvertible


@dataclass
class AskQuestionRequest(DictConvertible):
    question: str
    speak_answer: bool
