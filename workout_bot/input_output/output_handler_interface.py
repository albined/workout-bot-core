from abc import ABC, abstractmethod
from .message import Message

class OutputHandlerInterface(ABC):
    @abstractmethod
    async def send_message(self, message: Message):
        pass