from abc import ABC, abstractmethod
from LLM.LLMResult import LLMResult
from models.Message import Message

class LLMClientInterface(ABC):

    @abstractmethod
    def generate(self, messages: list[Message]) -> LLMResult:
        pass

