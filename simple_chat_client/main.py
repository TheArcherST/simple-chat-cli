from typing import Optional
from dataclasses import dataclass
import time
from argparse import Namespace
from long_state import LongStateObjectMixin, StatePlaceholder
import shlex
from commands_parser import build_parser
from config import command_handlers_registry, simple_chat_api, storage
from threading import Thread


@dataclass
class AuthInfo:
    username: Optional[str] = None


class Application(LongStateObjectMixin):
    auth_info: AuthInfo = StatePlaceholder("auth_info")

    def set_command_handler(self, ns: Namespace):
        if ns.set_key == 'username':
            self.auth_info.username = ns.set_value
            return f'auth_info.username={self.auth_info.username}'
        else:
            return f"неизвестная переменная {ns.set_key}"

    def get_command_handler(self, ns: Namespace):
        if ns.get_key == 'username':
            return self.auth_info.username
        else:
            return f"неизвестная переменная {ns.get_key}"

    def send_command_handler(self, ns: Namespace):
        my_username = self.auth_info.username

        if my_username is None:
            return "вы не указали ваш юзернейм в настройках авторизации"

        simple_chat_api.send_message(my_username, ns.chat, ns.send_text)

        return 'ok'


def update_daemon(app: Application):
    while True:
        time.sleep(1)
        with app:
            if app.auth_info.username is not None:
                updates = simple_chat_api.get_updates(app.auth_info.username)
                if not updates:
                    continue
                for i in updates:
                    print(f'{i.chat}: {i.text}')
                print('\n> ', end='')


def ui_daemon(app):
    parser = build_parser()

    command_handlers_registry.register_command_handler("set", app.set_command_handler)
    command_handlers_registry.register_command_handler("send", app.send_command_handler)
    command_handlers_registry.register_command_handler("get", app.get_command_handler)

    while True:
        time.sleep(0.1)
        command = input('\n> ')
        command = shlex.split(command)
        try:
            result = parser.parse_args(command)
        except SystemExit:
            pass
        else:
            with app:
                r = command_handlers_registry.process_command(result)
            print(r)


def main():
    app = Application(storage)
    threads = [
        Thread(target=ui_daemon, args=(app,)),
        Thread(target=update_daemon, args=(app,))
    ]
    for i in threads:
        i.start()
    for i in threads:
        i.join()


cli = main


if __name__ == '__main__':
    main()
