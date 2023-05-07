from typing import Callable, Optional
from dataclasses import dataclass
from argparse import Namespace


@dataclass
class Handler:
    filter: Callable[[Namespace], bool]
    handler: Callable[[Namespace], str]


class CommandHandlersRegistry:
    def __init__(self):
        self.handlers: list[Handler] = []

    def command_handler(self, command_name: Optional[str]):
        def deco(func):
            self.register_command_handler(command_name, func)
            return func
        return deco

    def register_command_handler(self, command_name: Optional[str], func):
        self.handlers.append(
            Handler(lambda x: x.subparser_name == command_name, func)
        )

    def process_command(self, ns: Namespace):
        for i in self.handlers:
            if i.filter(ns):
                return i.handler(ns)
