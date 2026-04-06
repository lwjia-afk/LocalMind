from enum import Enum

class Role(Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    TOOL = "tool"
    