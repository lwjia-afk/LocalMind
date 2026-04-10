from llm import baseLlmClient
from log_manager import LogManager
from models import Role
from models.message import message
from sessions.session_store import sessionsStore

logger = LogManager.get_logger(__name__)

class llmChatManager:

    def __init__(self, llm : baseLlmClient):
        self.llm = llm
        self.sessionstore = sessionsStore()

    def create_session(self, user: str = "default") -> str:
        sessionid = self.sessionstore.create_session(user = user)
        self.sessionstore.append_message(session_id= sessionid, role=Role.SYSTEM, content="You are a helpful assistant.")
        return sessionid

    def add_user_message(self, text, session_id: str, user: str = "default"):
        logger.info(f"User: {text}")
        self.sessionstore.append_message(session_id=session_id, role=Role.USER, content=text)

    def add_assistant_message(self, text, session_id: str, user: str = "default"):
        logger.info(f"Assistant: {text}")
        self.sessionstore.append_message(session_id=session_id, role=Role.ASSISTANT, content=text)

    def add_system_message(self, text, session_id: str, user: str = "default"):
        logger.info(f"System: {text}")
        self.sessionstore.append_message(session_id=session_id, role=Role.SYSTEM, content=text)

    def ask(self, text, session_id: str, user: str = "default") -> str:
        logger.info(f"Asking: {text}")
        self.add_user_message(text, session_id, user)
        res = self.llm.generate(self.sessionstore.get_history(session_id))
        self.add_assistant_message(res.text, session_id, user)
        return res.text
    
    def reset(self,session_id: str, system_prompt: str = None):
        self.sessionstore.delete_session(session_id)
        self.create_session(system_prompt, self.sessionstore.get_session(session_id).user)