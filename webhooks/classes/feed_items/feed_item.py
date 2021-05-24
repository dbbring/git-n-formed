# Global Modules
from __future__ import annotations
# Custom Modules
from ..readers.readers.reader_abstract import ReaderAbstract
from ..readers.reader_factory import ReaderFactory
from ..post_items.items import PostItem, AdItem
from ..discord_helpers.discord_webhook import DiscordMessageWrapper


class NoFeedItemReaderException(Exception):
    pass


class NoFeedItemException(Exception):
    pass


class FeedItem(object):

    _feed = {}
    message_wrappers = []
    _exisiting_links = {}
    reader: ReaderAbstract = None

    def __init__(self, feed: dict) -> None:
        if (feed is None):
            raise NoFeedItemException("No feed item was provided.")
        super().__init__()
        self._exisiting_links = feed['existing_links']
        self.message_wrappers = []
        self._feed = feed
        self.reader = ReaderFactory(self._feed['type']).reader
        self.__add_type_properties()
        self.__add_msg_wrappers()

        if self.reader is None:
            raise NoFeedItemReaderException('No reader present to get feed.')
        return

    def __add_msg_wrappers(self) -> None:
        channel: str = ''

        for channel in self._feed['channels']:
            msg_wrapper = DiscordMessageWrapper(channel, self._exisiting_links)
            self.message_wrappers.append(msg_wrapper)
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

    def get_messages(self, post_item: PostItem) -> None:
        msg: DiscordMessageWrapper = None
        msg_list: list = []

        for msg in self.message_wrappers:
            if self.__can_post(msg.channel, post_item) == False:
                continue

            msg = msg.get_DiscordMessage(post_item)
            if msg is not None:
                msg_list.append(msg)
        return msg_list

    def get_feed(self) -> FeedItem:
        if len(self._feed['url']) > 0:
            self.reader.fetch(self._feed['url'])
        return self

    def get_message_list(self) -> list:
        post: PostItem
        messages: list = []

        for post in self.reader.post_items:
            msgs = self.get_messages(post)
            messages += msgs
        return messages
