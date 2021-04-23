# Global Modules
import praw
import os
from dotenv import load_dotenv
import datetime
# Custom Modules
from .reader_abstract import ReaderAbstract
from ..post_items.post_item import PostItem


class NotAuthenticatedRedditExcpetion(Exception):
    pass


class RedditReader(ReaderAbstract):

    MAX_REDDIT_COMMENTS = 25
    __api = None
    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []
    # List[Post_Items]
    post_items = []
    properties = {
        "ups": 0
    }

    def __init__(self):
        super().__init__()
        load_dotenv()
        self.__api = praw.Reddit(
            client_id=os.getenv('REDDIT_API'),
            client_secret=os.getenv('REDDIT_API_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        return

    def __is_current_content(self, unix_datetime: float) -> bool:
        today = datetime.date.today()
        post_date = datetime.datetime.fromtimestamp(unix_datetime).date()

        if today == post_date:
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

    def _is_valid_link(self, link: str) -> bool:

        # additional checks here like already posted in chan

        if link == '':
            return False

        return True

    def _parse_content(self):
        self.__get_latest_content()
        for index, post in enumerate(self.post_items):
            if self._is_valid_link(post.link) == False:
                self.post_items.pop(index)
        return

    def fetch(self, url: str):
        subreddit = self.__api.subreddit(url)
        self._content_list = subreddit.new(limit=self.MAX_REDDIT_COMMENTS)
        self._parse_content()
        return self
