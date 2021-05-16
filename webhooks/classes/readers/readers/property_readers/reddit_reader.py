# Global Modules
from __future__ import annotations
import praw
import os
import datetime
# Custom Modules
from ._property_reader_abstract import PropertyReaderAbstract
from ....post_items.items import PostItem
from ....utils.string_utils import StringUtils


class NotAuthenticatedRedditExcpetion(Exception):
    pass


class RedditReader(PropertyReaderAbstract):

    __api = None
    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []
    # List[Post_Items]
    post_items = []
    # Optionable args from feeds json
    properties = {}

    def __init__(self):
        super().__init__()
        self.properties = {
            "ups": 0,
            "max_reddit_posts": 25
        }
        self.__api = praw.Reddit(
            client_id=os.getenv('REDDIT_API'),
            client_secret=os.getenv('REDDIT_API_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        return

    def __is_current_content(self, unix_datetime: float) -> bool:
        # Just case our time zones are mixed, checked for posts the next day
        today = datetime.date.today()
        tomarrow = today + datetime.timedelta(days=1)
        post_date = datetime.datetime.fromtimestamp(unix_datetime).date()

        if today == post_date or tomarrow == post_date:
            return True

        return False

    def __get_latest_content(self) -> None:
        for content in self._content_list:
            if content.ups >= self.properties["ups"]:
                if self.__is_current_content(content.created):
                    self.post_items.append(
                        self._to_post_item(content))
        return

    def _to_post_item(self, content):
        return PostItem(content='', link='https://www.reddit.com' + content.permalink)

    def _is_valid_link(self, post_item: PostItem) -> bool:
        if post_item.link == '':
            return False

        if StringUtils.extract_url(post_item.link) == '':
            return False

        return True

    def _parse_content(self) -> None:
        self.__get_latest_content()
        self.post_items = filter(self._is_valid_link, self.post_items)
        return None

    def fetch(self, url: str) -> RedditReader:
        subreddit = self.__api.subreddit(url)
        self._content_list = subreddit.new(
            limit=self.properties["max_reddit_posts"])
        self._parse_content()
        return self
