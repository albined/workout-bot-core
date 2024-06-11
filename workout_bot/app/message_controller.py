from ..input_output.message import Message, MessageType
from ..input_output.output_handler_interface import OutputHandlerInterface
from ..logic import MessageProcessor
from typing import Optional

class MessageController:
    def __init__(self, output_handler: OutputHandlerInterface, message_processor: Optional[MessageProcessor] = None) -> None:
        self.output_handler = output_handler
        if message_processor is None:
            message_processor = MessageProcessor()
        self.message_processor = message_processor
    
    async def handle_message(self, message: Message):
        response = await self.message_processor.process_message(message)
        if response.message_type == MessageType.TO_SEND:
            await self.output_handler.send_message(response)

    