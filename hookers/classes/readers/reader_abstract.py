# Global Modules
from abc import ABC, abstractmethod, abstractproperty
# Custom Modules
from ..post_items import post_item


class ReaderAbstract(ABC):

    @abstractproperty
    def post_items(self) -> list:
        # returns list of post items
        raise NotImplementedError()

    @abstractproperty
    def properties(self) -> dict:
        # returns dict of json settable dynamic properties for class use
        raise NotImplementedError()

    @abstractmethod
    def _to_post_item(self, feed_item) -> post_item.PostItem:
        # Custom implmentation should be converting to a universal post item
        raise NotImplementedError()

    @abstractmethod
    def fetch(self, url: str):
        # should populate post_items
        raise NotImplementedError()
