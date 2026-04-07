from abc import ABC, abstractmethod
from LLM.result import LLMResult
from models.message import Message

class BaseLLMClient(ABC):

    @abstractmethod
    def generate(self, messages: list[Message]) -> LLMResult:
        pass

