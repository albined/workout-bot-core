from abc import ABC, abstractmethod
from ..input_output.message import Message, MessageType
from typing import List, Optional

class Command(ABC):
    def __init__(self, db_handler) -> None:
        self.db_handler = db_handler

    @abstractmethod
    async def get_reply(self, message: Message) -> Message:
        pass

    @staticmethod
    @abstractmethod
    def aliases() -> Optional[List[str]]:
        pass

class CommandNotFound(Command):
    def __init__(self, db_handler=None) -> None:
        super().__init__(None)

    async def get_reply(self, message: Message) -> Message:
        reply = Message(
            message_type=MessageType.TO_SEND,
            message=f"Kunde inte hitta kommandot: {message.message}",
            recipients=[message.author]
        )
        return reply
    
    @staticmethod
    def aliases() -> List[str] | None:
        return
    
class Hej(Command):
    async def get_reply(self, message: Message) -> Message:
        reply = Message(
            message_type=MessageType.TO_SEND,
            message=f"Hej!",
            recipients=[message.author]
        )
        return reply
    
    @staticmethod
    def aliases() -> List[str] | None:
        return ['hej', 'hejsan', 'tjenare', 'tjena', 'hallå', 'hi']