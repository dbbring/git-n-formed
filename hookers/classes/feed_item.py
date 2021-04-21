from .readers.basic_ad_reader import BasicAdReader
from .readers.reader_abstract import ReaderAbstract
from .readers.reader_factory import ReaderFactory
from .post_items.post_item import PostItem
from .discord_helpers.discord_webhook import DiscordWebhook


class FeedItem(object):

    _reader: ReaderAbstract = None
    _feed = {}
    _webhooks = []

    def __init__(self, feed: dict, exisiting_links: dict = {}):
        super().__init__()
        self._webhooks = []
        self._feed = feed
        self._reader = ReaderFactory(self._feed['type']).reader

        for prop in self._feed["type_properties"].keys():
            self._reader.properties[prop] = self._feed["type_properties"][prop]

        for channel in self._feed['channels']:
            webhook = DiscordWebhook(channel)
            webhook.exisiting_links = exisiting_links
            self._webhooks.append(webhook)

        return

    def _post_to_discord(self, post_item: PostItem):
        webhook: DiscordWebhook

        for webhook in self._webhooks:
            channel_prefix = webhook.channel.split('-')[0]
            if (self._feed['type'] == 'basic-ad') and (channel_prefix == 'supporter'):
                continue

            webhook.post(post_item)
        return self

    def get_feed(self):
        if self._reader is not None and len(self._feed['url']) > 0:
            self._reader.fetch(self._feed['url'])
        return self

    def save(self):
        post: PostItem

        if self._reader is not None:
            for post in self._reader.post_items:
                self._post_to_discord(post)
        return self
