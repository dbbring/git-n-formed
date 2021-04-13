# Global Modules
import os
from typing import final
from discord import Webhook, RequestsWebhookAdapter
from dotenv import load_dotenv
# Custom Modules
from ..post_items.post_item import PostItem


class DiscordWebhook(object):

    _channel: str = ''
    _webhook: Webhook = None
    _exisiting_links = {}

    def __init__(self, channel: str):
        if len(channel) == 0:
            return

        self._channel = channel

        load_dotenv()

        self.__FREE_DEV: final = {
            'id': int(os.getenv('FREE_DEV_ID')),
            'token': os.getenv('FREE_DEV_TOKEN')
        }
        self.__SUPPORTER_DEV: final = {
            'id': int(os.getenv('SUPPORTER_DEV_ID')),
            'token': os.getenv('SUPPORTER_DEV_TOKEN')
        }
        self.__FREE_SECURITY: final = {
            'id': int(os.getenv('FREE_SECURITY_ID')),
            'token': os.getenv('FREE_SECURITY_TOKEN')
        }
        self.__SUPPORTER_SECURITY: final = {
            'id': int(os.getenv('SUPPORTER_SECURITY_ID')),
            'token': os.getenv('SUPPORTER_SECURITY_TOKEN')
        }
        self.__FREE_SYSTEMS: final = {
            'id': int(os.getenv('FREE_SYSTEMS_ID')),
            'token': os.getenv('FREE_SYSTEMS_TOKEN')
        }
        self.__SUPPORTER_SYSTEMS: final = {
            'id': int(os.getenv('SUPPORTER_SYSTEMS_ID')),
            'token': os.getenv('SUPPORTER_SYSTEMS_TOKEN')
        }
        self.__FREE_CLOUD: final = {
            'id': int(os.getenv('FREE_CLOUD_ID')),
            'token': os.getenv('FREE_CLOUD_TOKEN')
        }
        self.__SUPPORTER_CLOUD: final = {
            'id': int(os.getenv('SUPPORTER_CLOUD_ID')),
            'token': os.getenv('SUPPORTER_CLOUD_TOKEN')
        }
        self.__FREE_DEV_OPS: final = {
            'id': int(os.getenv('FREE_DEV_OPS_ID')),
            'token': os.getenv('FREE_DEV_OPS_TOKEN')
        }
        self.__SUPPORTER_DEV_OPS: final = {
            'id': int(os.getenv('SUPPORTER_DEV_OPS_ID')),
            'token': os.getenv('SUPPORTER_DEV_OPS_TOKEN')
        }
        self.__FREE_DATABASE: final = {
            'id': int(os.getenv('FREE_DATABASE_ID')),
            'token': os.getenv('FREE_DATABASE_TOKEN')
        }
        self.__SUPPORTER_DATABASE: final = {
            'id': int(os.getenv('SUPPORTER_DATABASE_ID')),
            'token': os.getenv('SUPPORTER_DATABASE_TOKEN')
        }

        self._routes = {
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

        self._webhook = Webhook.partial(
            self._routes[channel]['id'], self._routes[channel]['token'], adapter=RequestsWebhookAdapter())
        self._exisiting_links = DiscordGlobals().existing_links_global
        return

    def _build_msg(self, post: PostItem):
        return post.content + ' \n\n  ' + post.link

    def post(self, post_item: PostItem):
        if self._webhook is not None:
            msg = self._build_msg(post_item)
            self._webhook.send(content=msg, embed=post_item.embed)
