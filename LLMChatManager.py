from LLM import LLMClientInterface
from LogManager import LogManager
import pydoc
from ConfigManager import ConfigManager
from models import Role
from models.Message import Message


logger = LogManager.get_logger(__name__)

class LLMChatManager:

    def __init__(self, llm : LLMClientInterface, system_prompt: str = "You are a helpful assistant."):
        self.llm = llm
        self.history : list[Message] = []
        self.history.append(Message(role=Role.SYSTEM, content=system_prompt))


    def add_user_message(self, text):
        logger.info(f"User: {text}")
        self.history.append(Message(role=Role.USER, content=text))

    def add_assistant_message(self, text):
        logger.info(f"Assistant: {text}")
        self.history.append(Message(role=Role.ASSISTANT, content=text))

    def add_system_message(self, text):
        logger.info(f"System: {text}")
        self.history.append(Message(role=Role.SYSTEM, content=text))

    def ask(self, text):
        logger.info(f"Asking: {text}")
        self.add_user_message(text)
        res = self.llm.generate(self.history)
        self.add_assistant_message(res.text)
        return res.text
    
    def reset(self, system_prompt: str = None):
        self.history.clear()
        self.history.append(Message(role=Role.SYSTEM, content=system_prompt or "You are a helpful assistant."))