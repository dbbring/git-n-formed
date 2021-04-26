# Global Modules
from __future__ import annotations
import datetime
import feedparser
# Custom Modules
from ._property_reader_abstract import PropertyReaderAbstract
from ....post_items.post_item import PostItem
from ....utils.string_utils import StringUtils


class DateNotFoundRSSReaderException(Exception):
    pass


class RSSReader(PropertyReaderAbstract):

    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []
    # List[PostItem]
    post_items: list = []
    # Optionable args from feeds json
    properties = {}

    def __init__(self) -> None:
        self._content_list = []
        self.post_items = []
        self.properties = {
            "max_rss_entries": 10
        }
        return

    def __get_content_date(self, content) -> datetime:
        if hasattr(content, 'published_parsed'):
            return datetime.datetime(*(content.published_parsed[0:6])).date()

        if hasattr(content, 'updated'):
            date_str = StringUtils.extract_date(content.updated)
            if date_str != '':
                return datetime.datetime.strptime(date_str, '%Y-%m-%d')

        raise DateNotFoundRSSReaderException(
            "Could not find valid date attribute in RSS feed.")

    def __is_current_content(self, content) -> bool:
        today = datetime.date.today()
        post_date = self.__get_content_date(content)

        if today == post_date:
            return True

        return False

    def __get_latest_content(self) -> None:
        for content in self._content_list:
            if self.__is_current_content(content):
                self.post_items.append(
                    self._to_post_item(content))
        return

    def __parse_content(self) -> None:
        self.__get_latest_content()
        self.post_items = filter(self._is_valid_link, self.post_items)
        return None

    def _to_post_item(self, content_item) -> PostItem:
        return PostItem(content_item['title'], content_item['link'])

    def _is_valid_link(self, post_item: PostItem) -> bool:
        if post_item.link == '':
            return False

        if StringUtils.extract_url(post_item.link) == '':
            return False

        return True

    def fetch(self, rss_url: str) -> RSSReader:
        feed = feedparser.parse(rss_url)
        self._content_list = feed.entries[0:self.properties["max_rss_entries"]]
        self.__parse_content()
        return self
