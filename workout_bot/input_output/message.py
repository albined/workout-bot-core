from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class MessageType(Enum):
    NONE = 0
    RECIEVED = 1
    TO_SEND = 2

@dataclass
class Message:
    message_type: MessageType
    message: str
    author: Optional[str] = None
    recipients: List[int] = field(default_factory=list)
    image: Optional[bytes] = None