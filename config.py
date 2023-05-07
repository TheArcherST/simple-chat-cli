from core.handler_registry import CommandHandlersRegistry
from core.api_wrapper import SimpleChatAPI
from long_state import JsonStateStorage

command_handlers_registry = CommandHandlersRegistry()
simple_chat_api = SimpleChatAPI('https://dziroh.ru:8000')
storage = JsonStateStorage('data.json')
