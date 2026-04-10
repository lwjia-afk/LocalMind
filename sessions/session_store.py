import uuid
from models import Role
from models.message import message
from models.session import session

class sessionsStore():

    def __init__(self):
        self.session_store :list[session]  = {}

    def create_session(self,  user: str = "default") -> str:

        session_id = str(uuid.uuid4())
        self.session_store[session_id] = session(session_id=session_id, user=user)
        return session_id         
       
    def get_session(self, session_id: str = None, user: str = "default") -> session:
        if session_id is None:
            session_id = str(uuid.uuid4())
            self.create_session(session_id=session_id, user=user)
        return self.session_store.get(session_id)   
    
    def get_history(self, session_id: str) -> list[message]:
        session = self.get_session(session_id)
        return session.history


    def delete_session(self, session_id: str) -> None:
        """Delete the session with the given session_id."""
        self.session_store.pop(session_id, None)
    

    def append_message(self, session_id: str, role: Role, content: str, metadata: dict = None) -> None:
        """Append a message to the session with the given session_id."""
        session = self.get_session(session_id)
        session.append_message(message(role=role, content=content, metadata=metadata))

    def get_messages_content(self, session_id: str,) -> list:
        session = self.get_session(session_id)
        return [{"role": msg.role.value, "content": msg.content} for msg in session.history]
        