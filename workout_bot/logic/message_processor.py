from ..input_output.message import Message, MessageType

class MessageProcessor:
    async def process_message(self, message: Message) -> Message:
        new_message = Message(
            message_type=MessageType.TO_SEND,
            message="test_message",
        )
        return new_message
    