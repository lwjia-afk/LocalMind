from abc import ABC, abstractmethod
from .result import llmResult
from models.message import message

class baseLlmClient(ABC):

    @abstractmethod
    def generate(self, messages: list[message]) -> llmResult:
        pass

