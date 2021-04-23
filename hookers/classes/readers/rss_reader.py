# Type Hinting
from __future__ import annotations
from typing import final
# Global Modules
import datetime
import feedparser
# Custom Modules
from .reader_abstract import ReaderAbstract
from ..post_items.post_item import PostItem
from ..utils.string_utils import StringUtils


class DateNotFoundRSSReaderExcpetion(Exception):
    pass


class RSSReader(ReaderAbstract):

    MAX_RSS_ENTRIES: final = 10
    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []
    # List[PostItem]
    post_items: list = []
    properties = {}

    def __init__(self):
        self._content_list = []
        self.post_items = []
        return

    def __get_content_date(self, content):
        if hasattr(content, 'published_parsed'):
            return datetime.datetime(*(content.published_parsed[0:6])).date()

        if hasattr(content, 'updated'):
            date_str = StringUtils.extract_date(content.updated)
            if date_str != '':
                return datetime.datetime.strptime(date_str, '%Y-%m-%d')

        raise DateNotFoundRSSReaderExcpetion(
            "Could not find valid date attribute in RSS feed.")

    def __is_current_content(self, content) -> bool:
        today = datetime.date.today()
        post_date = self.__get_content_date(content)

        if today == post_date:
            return True

        return False

    def __get_latest_content(self) -> int:
        for content in self._content_list:
            if self.__is_current_content(content):
                self.post_items.append(
                    self._to_post_item(content))
        return len(self._content_list)

    def _to_post_item(self, content_item) -> PostItem:
        return PostItem(content_item['title'], content_item['link'])

    def _is_valid_link(self, link: str) -> bool:
        isValid = False

        # additional checks here like already posted in chan

        if link != '':
            isValid = True

        return isValid

    def __fetch_content(self) -> None:
        self.__get_latest_content()
        for index, post in enumerate(self.post_items):
            if self._is_valid_link(post.link) == False:
                self.post_items.pop(index)
        return None

    def fetch(self, rss_url: str) -> RSSReader:
        feed = feedparser.parse(rss_url)
        self._content_list = feed.entries[0:self.MAX_RSS_ENTRIES]
        self.__fetch_content()
        return self
