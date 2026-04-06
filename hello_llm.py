import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from LLM import OllamaClient
from LLMChatManager import LLMChatManager
import logging
from LogManager import LogManager
from ConfigManager import ConfigManager

config = ConfigManager.load_config()


LogManager.init()
logger = LogManager.get_logger(__name__)

logger.info("Starting AI agentic")

llm = OllamaClient()
chat = LLMChatManager(llm)

print(chat.ask("写一个诗歌，题目是春天"))
