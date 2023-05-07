from core.handler_registry import CommandHandlersRegistry
from core.api_wrapper import SimpleChatAPI
from long_state import JsonStateStorage

command_handlers_registry = CommandHandlersRegistry()
simple_chat_api = SimpleChatAPI('http://0.0.0.0:8000')
storage = JsonStateStorage('data.json')
