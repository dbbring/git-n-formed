# Global Modules
from __future__ import annotations
# Custom Modules
from ._property_reader_abstract import PropertyReaderAbstract
from ....post_items.items import PostItem, AdItem
from ....utils.string_utils import StringUtils


class BasicAdReader(PropertyReaderAbstract):

    # List[PostItem]
    post_items: list = []
    # Optionable Props from feed json
    properties = {}

    def __init__(self) -> None:
        self.post_items = []
        self.properties = {
            "message": ""
        }
        return

    def _to_post_item(self, url) -> PostItem:
        return AdItem(self.properties["message"], url)

    def _is_valid_link(self, post_item: PostItem) -> bool:
        if post_item.link == '':
            return False

        if StringUtils.extract_url(post_item.link) == '':
            return False

        return True

    def fetch(self, url: str) -> BasicAdReader:
        self.post_items.append(self._to_post_item(url))
        self.post_items = filter(self._is_valid_link, self.post_items)
        return self
