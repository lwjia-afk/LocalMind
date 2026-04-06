from venv import logger

import requests
from models.Message import Message
from LLM.LLMResult import LLMResult
from LLM.LLMClient.LLMClientInterface import LLMClientInterface
from LogManager import LogManager
from ConfigManager import ConfigManager

logger = LogManager.get_logger(__name__)


class OllamaClient(LLMClientInterface):
 
    def __init__(self):
        self.generate_url = ConfigManager.get("llm.ollama.generate_url")
        self.model = ConfigManager.get("llm.ollama.model")  


    def generate(self, messages: list[Message]) -> LLMResult: 
        logger.info(f"LLMOllama generate called with messages: {messages}, url: {self.generate_url}, model: {self.model}")


        data = {
            "model": self.model,
            "messages": [{"role": msg.role.value, "content": msg.content} for msg in messages],
            "stream": False
        }
        print(f"before requests.post: url={self.generate_url}, data={data}")
        res = requests.post(self.generate_url, json=data)

        if res.status_code != 200:
            logger.error(f"Failed to call LLM API. Status code: {res.status_code}, res: {res.text}")
            raise Exception(f"Failed to call LLM API. Status code: {res.status_code}, res: {res.text}")

        return LLMResult(
            text=res.json()["message"]["content"],
            raw=res.json())