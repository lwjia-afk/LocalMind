from LLM import LLMClientInterface
from LLM import LLMResult

class fakeLLMClient(LLMClientInterface):
    def __init__(self):
        pass

    def generate(self, messages: list) -> LLMResult:
        res = LLMResult(text="This is a fake response from the fakeLLMClient.", raw={})
        return res