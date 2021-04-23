from .reader_abstract import ReaderAbstract
from ..post_items.post_item import PostItem


class BasicAdReader(ReaderAbstract):

    # List[PostItem]
    post_items: list = []
    properties = {
        "message": ""
    }

    def __init__(self):
        self._content_list = []
        self.post_items = []
        return

    def _to_post_item(self, url) -> PostItem:
        return PostItem(self.properties["message"], url)

    def _is_valid_link(self, link: str) -> bool:
        isValid = False

        # additional checks here like already posted in chan

        if link != '':
            isValid = True

        return isValid

    def fetch(self, url: str):
        self.post_items.append(self._to_post_item(url))
        return self
