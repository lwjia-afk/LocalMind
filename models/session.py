from dataclasses import dataclass, field
from models.message import message

class session:
    session_id: str
    user: str
    history: list[message] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def __init__(self, session_id: str, user: str, message: message = None, metadata: dict = None):
        self.session_id = session_id
        self.user = user
        self.history = [message] if message else []
        self.metadata = metadata if metadata else {}

    def append_message(self, message: message):
        self.history.append(message)    
    
    def get_history(self) -> list[message]:
        return self.history
    


    