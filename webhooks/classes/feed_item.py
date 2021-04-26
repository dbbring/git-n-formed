# Global Modules
from __future__ import annotations
# Custom Modules
from .readers.readers.reader_abstract import ReaderAbstract
from .readers.reader_factory import ReaderFactory
from .post_items.post_item import PostItem
from .discord_helpers.discord_webhook import DiscordWebhook


class NoFeedItemReaderException(Exception):
    pass


class FeedItem(object):

    _reader: ReaderAbstract = None
    _feed = {}
    _webhooks = []

    def __init__(self, feed: dict, exisiting_links: dict = {}) -> None:
        super().__init__()
        self._webhooks = []
        self._feed = feed
        self._reader = ReaderFactory(self._feed['type']).reader
        self.__add_type_properties()
        self.__add_webhooks(exisiting_links)

        if self._reader is None:
            raise NoFeedItemReaderException('No reader present to get feed.')
        return

    def __add_webhooks(self, exisiting_links) -> None:
        channel: str = ''

        for channel in self._feed['channels']:
            webhook = DiscordWebhook(channel, exisiting_links)
            self._webhooks.append(webhook)
        return

    def __add_type_properties(self) -> None:
        prop: dict = {}

        if "type_properties" in self._feed.keys():
            for prop in self._feed["type_properties"].keys():
                self._reader.properties[prop] = self._feed["type_properties"][prop]
        return

    def _post_to_discord(self, post_item: PostItem) -> None:
        webhook: DiscordWebhook = None
        channel_prefix: str = ''

        for webhook in self._webhooks:
            channel_prefix = webhook.channel.split('-')[0]
            if (self._feed['type'] == 'basic-ad') and (channel_prefix == 'supporter'):
                continue

            webhook.post(post_item)
        return

    def get_feed(self) -> FeedItem:
        if len(self._feed['url']) > 0:
            self._reader.fetch(self._feed['url'])
        return self

    def save(self) -> FeedItem:
        post: PostItem

        for post in self._reader.post_items:
            self._post_to_discord(post)
        return self
