from core.handler_registry import CommandHandlersRegistry
from core.api_wrapper import SimpleChatAPI
from core.long_state import MemoryStateStorage

command_handlers_registry = CommandHandlersRegistry()
simple_chat_api = SimpleChatAPI('https://dziroh.ru:8000')
storage = MemoryStateStorage()
