from dataclasses import dataclass
from dataclass_factory import Factory
from aiohttp import ClientSession, TCPConnector


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

    async def send_message(
            self,
            my_username: str,
            chat: str,
            text: str,
    ):

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:

            r = await session.get(
                APIMethods.send_message.get_url(self.base_url),
                params={'text': text,
                        'chat': chat,
                        'my_username': my_username}
            )

            if r.status != 200:
                raise SimpleChatAPIError(f"Error from API, while trying to send message: {await r.json()} [{r.status}]")
            else:
                return None

    async def get_updates(
            self,
            my_username: str,
    ) -> list[Message]:

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            r = await session.get(
                APIMethods.get_updates.get_url(self.base_url),
                params={'my_username': my_username}
            )

            if r.status != 200:
                raise SimpleChatAPIError(f"Error from API, while trying to get updates: {r.json()} [{r.status}]")
            else:
                data = await r.json()
                factory = Factory()
                result = factory.load(data, list[Message])
                return result
