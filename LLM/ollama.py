from venv import logger

import requests
from models.message import message
from llm.result import llmResult
from llm.base import baseLlmClient
from log_manager import LogManager
from config_manager import ConfigManager

logger = LogManager.get_logger(__name__)


class ollamaClient(baseLlmClient):
 
    def __init__(self):
        self.generate_url = ConfigManager.get("llm.ollama.generate_url")
        self.model = ConfigManager.get("llm.ollama.model")  


    def generate(self, messages: list[message]) -> llmResult: 
        logger.info(f"ollamaClient generate called with messages: {messages}, url: {self.generate_url}, model: {self.model}")


        data = {
            "model": self.model,
            "messages": [{"role": msg.role.value, "content": msg.content} for msg in messages],
            "stream": False
        }
        print(f"before requests.post: url={self.generate_url}, data={data}")
        
        try:
            res = requests.post(self.generate_url, json=data)
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Cannot connect to Ollama at {self.generate_url}. Is Olla running? ")
            raise ConnectionError(f"Cannot connect to Ollama at {self.generate_url}. "
                                  "running ( run 'ollama serve' in a terminal).") from e

        if res.status_code != 200:
            logger.error(f"Failed to call LLM API. Status code: {res.status_code}, res: {res.text}")
            raise Exception(f"Failed to call LLM API. Status code: {res.status_code}, res: {res.text}")

        return llmResult(
            text=res.json()["message"]["content"],
            raw=res.json())