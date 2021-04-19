# Global Modules
import os
from typing import final
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
# Custom Modules
from ..post_items.post_item import PostItem


class DiscordRoutes(object):

    _channels: dict = {}

    def __init__(self) -> None:
        load_dotenv()

        self.__FREE_DEV: final = {
            'id': int(os.getenv('FREE_DEV_ID')),
            'token': os.getenv('FREE_DEV_TOKEN'),
            'chan_id': os.getenv('FREE_DEV_CHAN_ID')
        }
        self.__SUPPORTER_DEV: final = {
            'id': int(os.getenv('SUPPORTER_DEV_ID')),
            'token': os.getenv('SUPPORTER_DEV_TOKEN'),
            'chan_id': os.getenv('SUPPORTER_DEV_CHAN_ID')
        }
        self.__FREE_SECURITY: final = {
            'id': int(os.getenv('FREE_SECURITY_ID')),
            'token': os.getenv('FREE_SECURITY_TOKEN'),
            'chan_id': os.getenv('FREE_SECURITY_CHAN_ID')
        }
        self.__SUPPORTER_SECURITY: final = {
            'id': int(os.getenv('SUPPORTER_SECURITY_ID')),
            'token': os.getenv('SUPPORTER_SECURITY_TOKEN'),
            'chan_id': os.getenv('SUPPORTER_SECURITY_CHAN_ID')
        }
        self.__FREE_SYSTEMS: final = {
            'id': int(os.getenv('FREE_SYSTEMS_ID')),
            'token': os.getenv('FREE_SYSTEMS_TOKEN'),
            'chan_id': os.getenv('FREE_SYSTEMS_CHAN_ID')
        }
        self.__SUPPORTER_SYSTEMS: final = {
            'id': int(os.getenv('SUPPORTER_SYSTEMS_ID')),
            'token': os.getenv('SUPPORTER_SYSTEMS_TOKEN'),
            'chan_id': os.getenv('SUPPORTER_SYSTEMS_CHAN_ID')
        }
        self.__FREE_CLOUD: final = {
            'id': int(os.getenv('FREE_CLOUD_ID')),
            'token': os.getenv('FREE_CLOUD_TOKEN'),
            'chan_id': os.getenv('FREE_CLOUD_CHAN_ID')
        }
        self.__SUPPORTER_CLOUD: final = {
            'id': int(os.getenv('SUPPORTER_CLOUD_ID')),
            'token': os.getenv('SUPPORTER_CLOUD_TOKEN'),
            'chan_id': os.getenv('SUPPORTER_CLOUD_CHAN_ID')
        }
        self.__FREE_DEV_OPS: final = {
            'id': int(os.getenv('FREE_DEV_OPS_ID')),
            'token': os.getenv('FREE_DEV_OPS_TOKEN'),
            'chan_id': os.getenv('FREE_DEV_OPS_CHAN_ID')
        }
        self.__SUPPORTER_DEV_OPS: final = {
            'id': int(os.getenv('SUPPORTER_DEV_OPS_ID')),
            'token': os.getenv('SUPPORTER_DEV_OPS_TOKEN'),
            'chan_id': os.getenv('SUPPORTER_DEV_OPS_CHAN_ID')
        }
        self.__FREE_DATABASE: final = {
            'id': int(os.getenv('FREE_DATABASE_ID')),
            'token': os.getenv('FREE_DATABASE_TOKEN'),
            'chan_id': os.getenv('FREE_DATABASE_CHAN_ID')
        }
        self.__SUPPORTER_DATABASE: final = {
            'id': int(os.getenv('SUPPORTER_DATABASE_ID')),
            'token': os.getenv('SUPPORTER_DATABASE_TOKEN'),
            'chan_id': os.getenv('SUPPORTER_DATABASE_CHAN_ID')
        }

        self._channels = {
            'free-dev': self.__FREE_DEV,
            'supporter-dev': self.__SUPPORTER_DEV,
            'free-security': self.__FREE_SECURITY,
            'supporter-security': self.__SUPPORTER_SECURITY,
            'free-systems': self.__FREE_SYSTEMS,
            'supporter-systems': self.__SUPPORTER_SYSTEMS,
            'free-cloud': self.__FREE_CLOUD,
            'supporter-cloud': self.__SUPPORTER_CLOUD,
            'free-dev-ops': self.__FREE_DEV_OPS,
            'supporter-dev-ops': self.__SUPPORTER_DEV_OPS,
            'free-database': self.__FREE_DATABASE,
            'supporter-database': self.__SUPPORTER_DATABASE
        }
        return

    def get_all_channels(self) -> list:
        return self._channels.keys()

    def get_channel_id(self, channel: str) -> int:
        return int(self._channels[channel]['chan_id'])


class DiscordWebhook(DiscordRoutes):

    _channel: str = ''
    _webhook: Webhook = None

    def __init__(self, channel: str):
        if len(channel) == 0:
            return

        super().__init__()
        self._webhook = Webhook.partial(
            super()._channels[channel]['id'], super()._channels[channel]['token'], adapter=RequestsWebhookAdapter())
        return

    def _build_msg(self, post: PostItem):
        return post.content + ' \n\n  ' + post.link

    def post(self, post_item: PostItem):
        if self._webhook is not None:
            msg = self._build_msg(post_item)
            self._webhook.send(content=msg, embed=post_item.embed)
