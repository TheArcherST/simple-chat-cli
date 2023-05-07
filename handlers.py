from config import simple_chat_api, command_handlers_registry


@command_handlers_registry.register_command_handler(None)
def root_handler(ns):
    return "Hello!"


@command_handlers_registry.register_command_handler("set")
def set_command_handler(ns):
    return f'{ns.set_key}={ns.set_value}'


@command_handlers_registry.register_command_handler("send")
def send_command_handler(ns):
    return f'message sent'
