from dataclasses import dataclass
from dataclass_factory import Factory
import requests


class SimpleChatAPIError(Exception):
    pass


@dataclass
class Message:
    id: int
    from_user: str
    chat: str
    text: str


@dataclass
class _APIMethod:
    api_version: int = None
    method_name: str = None

    def get_url(self, base_url: str):
        return f'{base_url}/v{self.api_version}/{self.method_name}'


class APIMethods:
    send_message = _APIMethod(1, "sendMessage")
    get_updates = _APIMethod(1, "getUpdates")


class SimpleChatAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def send_message(
            self,
            my_username: str,
            chat: str,
            text: str,
    ):

        r = requests.get(
            APIMethods.send_message.get_url(self.base_url),
            params={'text': text,
                    'chat': chat,
                    'my_username': my_username}
        )

        if r.status_code != 200:
            raise SimpleChatAPIError(f"Error from API, while trying to send message: {r.json()} [{r.status_code}]")
        else:
            return None

    def get_updates(
            self,
            my_username: str,
    ) -> list[Message]:

        r = requests.get(
            APIMethods.get_updates.get_url(self.base_url),
            params={'my_username': my_username}
        )

        if r.status_code != 200:
            raise SimpleChatAPIError(f"Error from API, while trying to get updates: {r.json()} [{r.status_code}]")
        else:
            data = r.json()
            factory = Factory()
            result = factory.load(data, list[Message])
            return result
