# Global Modules
import os
import discord
import re
from dotenv import load_dotenv
# Custom Modules
from .discord_webhook import DiscordRoutes


class DiscordAPIClient(object):

    __MAX_MESSAGE_LIMIT = 500
    __client: discord.Client = None
    _routes: DiscordRoutes = None
    channel_history: dict = {}  # {'channel': set(links: str)}

    def __init__(self) -> None:
        super().__init__()
        load_dotenv()
        self.__client = discord.Client()
        self._routes = DiscordRoutes()
        return None

    def __process_func(self, async_function):

        @self.__client.event
        async def on_ready():
            await async_function
            await self.__client.close()
            return

        self.__client.run(os.getenv('DISCORD_API_TOKEN'))

    async def __fetch_messages(self):
        for channel in self._routes.get_all_channels():
            chan_id = self._routes.get_channel_id(channel)
            discord_channel = self.__client.guilds[0].get_channel(chan_id)

            if discord_channel is not None:
                messages = await discord_channel.history(limit=self.__MAX_MESSAGE_LIMIT).flatten()
                self.channel_history[channel] = messages

    def __sanitize_url(self, dirty_url: str) -> str:
        if len(dirty_url) == 0:
            return ''

        clean_url = dirty_url.replace('https', '')
        clean_url = clean_url.replace('http', '')
        clean_url = clean_url.replace('://www.', '')
        clean_url = clean_url.replace('://', '')

        if clean_url[len(clean_url) - 1] == '/':
            clean_url = clean_url[0:len(clean_url) - 1]

        return clean_url

    def __find_url(self, message_content: str) -> str:
        pattern = re.compile(
            r"(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?")
        result = pattern.search(message_content)

        if result == None:
            return ''

        return result.group(0)

    def __extract_url(self, message_content):
        url = self.__find_url(message_content)
        url = self.__sanitize_url(url)
        return url

    def __process_channel_messages(self, message_list: list) -> set:
        sanitized_url_list = set()
        for message in message_list:
            content = message.content
            url = self.__extract_url(content)
            if url != '':
                sanitized_url_list.add(url)
        return sanitized_url_list

    def __process_messages(self):
        for channel in self.channel_history.keys():
            channel_messages = self.channel_history[channel]
            self.channel_history[channel] = self.__process_channel_messages(
                channel_messages)
        return

    def get_existing_links(self):
        self.__process_func(self.__fetch_messages())
        self.__process_messages()
        return self.channel_history
