# Global Modules
import os
from typing import final
import discord as discord_python
from typing import final, Callable
# Custom Modules
from .discord_webhook import DiscordRoutes
from ..utils.string_utils import StringUtils


class DiscordAPIClient(object):

    __MAX_MESSAGE_LIMIT: final = 500
    __client: discord_python.Client = None
    _routes: DiscordRoutes = None
    channel_history: dict = {}  # {'channel': set(links: str)}

    def __init__(self) -> None:
        super().__init__()
        self.__client = discord_python.Client()
        self._routes = DiscordRoutes()
        return None

    def __process_func(self, async_function: Callable[[], None]) -> None:

        @self.__client.event
        async def on_ready():
            await async_function
            await self.__client.close()
            return

        self.__client.run(os.getenv('DISCORD_API_TOKEN'))
        return

    async def __fetch_messages(self) -> None:
        for channel in self._routes.get_all_channels():
            chan_id = self._routes.get_channel_id(channel)
            discord_channel = self.__client.guilds[0].get_channel(chan_id)

            if discord_channel is not None:
                messages = await discord_channel.history(limit=self.__MAX_MESSAGE_LIMIT).flatten()
                self.channel_history[channel] = messages
        return

    def __process_channel_messages(self, message_list: list) -> set:
        sanitized_url_list = set()
        for message in message_list:
            content = message.content
            url = StringUtils.sanitize_url(StringUtils.extract_url(content))
            if url != '':
                sanitized_url_list.add(url)
        return sanitized_url_list

    def __process_messages(self) -> dict:
        for channel in self.channel_history.keys():
            channel_messages = self.channel_history[channel]
            self.channel_history[channel] = self.__process_channel_messages(
                channel_messages)
        return self.channel_history

    def get_existing_links(self) -> dict:
        self.__process_func(self.__fetch_messages())
        return self.__process_messages()
