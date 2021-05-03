# Global Modules
from __future__ import annotations
# Custom Modules
from .readers.readers.reader_abstract import ReaderAbstract
from .readers.reader_factory import ReaderFactory
from .post_items.items import PostItem, AdItem
from .discord_helpers.discord_webhook import DiscordWebhook


class NoFeedItemReaderException(Exception):
    pass


class NoFeedItemException(Exception):
    pass


class FeedItem(object):

    __postAd: bool = False
    _feed = {}
    _webhooks = []
    _exisiting_links = {}
    reader: ReaderAbstract = None

    def __init__(self, feed: dict) -> None:
        if (feed is None):
            raise NoFeedItemException("No feed item was provided.")
        super().__init__()
        self.__postAd = False
        self._exisiting_links = feed['existing_links']
        self._webhooks = []
        self._feed = feed
        self.reader = ReaderFactory(self._feed['type']).reader
        self.__add_type_properties()
        self.__add_webhooks()

        if self.reader is None:
            raise NoFeedItemReaderException('No reader present to get feed.')
        return

    def __add_webhooks(self) -> None:
        channel: str = ''

        for channel in self._feed['channels']:
            webhook = DiscordWebhook(channel, self._exisiting_links)
            self._webhooks.append(webhook)
        return

    def __add_type_properties(self) -> None:
        prop: dict = {}

        if "type_properties" in self._feed.keys():
            for prop in self._feed["type_properties"].keys():
                self.reader.properties[prop] = self._feed["type_properties"][prop]
        return

    def __can_post_ad(self, channel: str, ad_item: PostItem) -> bool:
        channel_prefix = channel.split('-')[0]
        if (self._feed['type'] == 'basic-ad') and (channel_prefix == 'supporter'):
            return False

        return True

    def __can_post(self, channel: str, post_item: PostItem) -> bool:
        if isinstance(post_item, AdItem):
            return self.__can_post_ad(channel, post_item)

        return True

    def _save_ad(self):
        if self._feed['ad'] is not None:
            ad = FeedItem(self._feed['ad'])
            ad.get_feed()

            for post in ad.reader.post_items:
                ad.post_to_discord(post)
        return

    def post_to_discord(self, post_item: PostItem) -> None:
        webhook: DiscordWebhook = None

        for webhook in self._webhooks:
            if self.__can_post(webhook.channel, post_item) == False:
                continue

            if webhook.post(post_item):
                self.__postAd = True
        return

    def get_feed(self) -> FeedItem:
        if len(self._feed['url']) > 0:
            self.reader.fetch(self._feed['url'])
        return self

    def save(self) -> FeedItem:
        post: PostItem

        for post in self.reader.post_items:
            self.post_to_discord(post)

        if self.__postAd:
            self._save_ad()
        return self
