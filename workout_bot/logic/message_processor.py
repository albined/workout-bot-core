from ..input_output.message import Message, MessageType
import re
from typing import List
from .commands import Command, CommandNotFound
from ..data_access.database_handler import DatabaseHandler
import importlib
import inspect
import logging

class MessageProcessor:
    def __init__(self) -> None:
        self.db_handler = DatabaseHandler()
        self.command_not_found = CommandNotFound()
        self.commands = self.load_commands()
        # Add commands to dictionary for easy fetching
        self.command_dict = {}
        for command in self.commands:
            if command.aliases() is None:
                continue
            for alias in command.aliases():
                alias = self.clean_text_(alias)
                if alias in self.command_dict:
                    logging.warn(f'Alias {alias} is defined multiple times')
                self.command_dict[alias] = command

    def load_commands(self) -> List[Command]:
        commands_module = importlib.import_module('.commands', __package__)
        commands = []
        for name, obj in inspect.getmembers(commands_module):
            if inspect.isclass(obj) and issubclass(obj, Command) and obj is not Command:
                commands.append(obj(self.db_handler))
        return commands    

    async def process_message(self, message: Message) -> Message:
        message_text = self.clean_text_(message.message)
        message_command =  self.find_command(message_text)
        reply = await message_command.get_reply(message)
        return reply
    
    def find_command(self, message_txt: str) -> Command:
        return self.command_dict.get(message_txt, self.command_not_found)

    def clean_text_(self, text: str) -> str:
        # lowers charachters and removes non alphabet or numbers
        result = text.lower()
        result = re.sub(r'[^a-z0-9åäö]', '', result)
        return result
    
    