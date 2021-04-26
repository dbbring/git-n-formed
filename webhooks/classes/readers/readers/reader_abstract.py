# Global Modules
from abc import ABC, abstractmethod, abstractproperty
# Custom Modules
from ...post_items.post_item import PostItem


class ReaderAbstract(ABC):

    @abstractproperty
    def post_items(self) -> list:
        # returns list of post items
        raise NotImplementedError()

    @abstractmethod
    def _to_post_item(self, feed_item) -> PostItem:
        # Custom implmentation should be converting to a universal post item
        raise NotImplementedError()

    @abstractmethod
    def fetch(self, url: str):
        # should populate post_items
        raise NotImplementedError()
