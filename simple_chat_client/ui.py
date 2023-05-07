import asyncio
import datetime

from textual.widget import Widget
from textual.containers import VerticalScroll, Horizontal
from textual.widgets import Header, Footer, Input, Label
from textual.app import App, ComposeResult
from dataclasses import dataclass, field
from threading import Thread
from argparse import ArgumentParser

from .api_wrapper import SimpleChatAPI, Message


simple_chat_api = SimpleChatAPI('https://dziroh.ru:8000')


@dataclass
class PendingMessage:
    text: str


@dataclass
class SharedContainer:
    my_username: str = None
    chat: str = None
    history: list[Message] = field(default_factory=list)
    send_pending: list[PendingMessage] = field(default_factory=list)


shared_container = SharedContainer()


def get_message_by_id(id_: int):
    for i in shared_container.history:
        if i.id == id_:
            return i


def is_me_username(username) -> bool:
    return username == shared_container.my_username


class MessageInput(Input):
    def on_mount(self):
        self.styles.margin = 1


class MessageUsername(Label):
    def __init__(self, username: str):

        self.username = username

        super().__init__(username)

    def on_mount(self):
        self.styles.width = 15
        self.styles.text_align = 'right'

        if is_me_username(self.username):
            self.styles.color = '#0087ff'
            self.styles.text_style = 'b'


class MessageText(Label):
    def on_mount(self):
        self.styles.padding = (0, 0, 0, 3)


class MessageWidget(Widget):
    def __init__(self, message_id: int):

        self.message_id = message_id

        super().__init__()

    def compose(self) -> ComposeResult:
        message = get_message_by_id(self.message_id)
        yield Horizontal(
            MessageUsername(message.from_user),
            MessageText(message.text),
        )

    def on_mount(self):
        self.styles.height = 1


class MessageHistoryContainer(Widget):
    def compose(self):
        yield VerticalScroll()

    def on_mount(self):
        self.styles.height = "80%"
        self.styles.margin = 1


class SimpleChatApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield MessageHistoryContainer()
        yield MessageInput(placeholder="Message", id='message_input')
        yield Footer()

    def synchronize_messages(self):
        self.query(MessageWidget).remove()
        messages_container = self.query_one(MessageHistoryContainer)
        messages_container.children[0].mount_all((
            MessageWidget(i.id)
            for i in shared_container.history
        ))

    def on_input_submitted(self, _event):
        message_input = self.query_one(MessageInput)
        shared_container.send_pending.append(PendingMessage(
            message_input.value
        ))
        message_input.value = ""

    def on_mount(self):
        self.run_worker(synchronisation_daemon(self))


async def synchronisation_daemon(app: SimpleChatApp):
    while True:
        await asyncio.sleep(0.1)

        for i in shared_container.send_pending.copy():
            await simple_chat_api.send_message(
                my_username=shared_container.my_username,
                chat=shared_container.chat,
                text=i.text,
            )
            shared_container.send_pending.remove(i)
            shared_container.history.append(
                Message(int(datetime.datetime.now().timestamp()), shared_container.my_username, shared_container.chat, i.text)
            )
            app.synchronize_messages()

        updates = await simple_chat_api.get_updates(shared_container.my_username)
        shared_container.history.extend(updates)
        if updates:
            app.synchronize_messages()


def main():
    parser = ArgumentParser()
    parser.add_argument("my_username")
    parser.add_argument("chat")
    ns = parser.parse_args()

    shared_container.my_username = ns.my_username
    shared_container.chat = ns.chat

    app = SimpleChatApp()

    threads = [Thread(target=synchronisation_daemon, args=(app,))]

    for i in threads:
        i.start()

    app.run()


cli = main
