from models.role import Role
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    role: Role
    content: str
    timestamp: datetime = datetime.now()
    metadata: dict[str, any] = None
    
        

    