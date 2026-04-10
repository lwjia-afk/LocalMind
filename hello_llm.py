import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from llm import ollamaClient
from chat_manager import llmChatManager
from log_manager import LogManager
from config_manager import ConfigManager

config = ConfigManager.load_config()


LogManager.init()
logger = LogManager.get_logger(__name__)

logger.info("Starting AI agentic")

llm = ollamaClient()
chat = llmChatManager(llm)
session_id=chat.create_session()


print(chat.ask("写一个诗歌，题目是春天", session_id=session_id))
