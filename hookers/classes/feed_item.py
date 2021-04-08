from .readers.reader_abstract import ReaderAbstract
from .readers.reader_factory import ReaderFactory
from .post_items.post_item import PostItem
from .discord_webhooks.discord_webhook import DiscordWebhook


class FeedItem(object):

    _reader: ReaderAbstract = None
    _feed = {}
    _webhooks = []

    def __init__(self, feed: dict):
        super().__init__()
        self._webhooks = []
        self._feed = feed
        self._reader = ReaderFactory(self._feed['type']).reader
        for channel in self._feed['channels']:
            self._webhooks.append(DiscordWebhook(channel))
        return

    def _post_to_discord(self, msg: str):
        webhook: DiscordWebhook

        for webhook in self._webhooks:
            webhook.post(msg)
        return self

    def _build_msg(self, post: PostItem):
        return post.content + ' \n\n  ' + post.link

    def get_feed(self):
        if self._reader is not None and len(self._feed['url']) > 0:
            self._reader.fetch(self._feed['url'])
        return self

    def save(self):
        post: PostItem

        if self._reader is not None:
            for post in self._reader.post_items:
                msg = self._build_msg(post)
                self._post_to_discord(msg)
        return self
