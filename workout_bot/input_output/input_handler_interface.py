from abc import ABC, abstractmethod
from .message import Message
from ..app.message_controller import MessageController

class InputHandlerInterface(ABC):
    def __init__(self, message_controller: MessageController) -> None:
        self.message_controller = message_controller

    @abstractmethod
    async def receive_message(self, message: Message):
        pass