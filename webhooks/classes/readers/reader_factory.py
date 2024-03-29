# Global Modules

# Custom Modules
from .readers.reader_abstract import ReaderAbstract
from .readers.property_readers.rss_reader import RSSReader
from .readers.property_readers.twitter_reader import TwitterReader
from .readers.property_readers.reddit_reader import RedditReader
from .readers.property_readers.basic_ad_reader import BasicAdReader


class ReaderFactoryNotFoundException(Exception):
    pass


class ReaderFactory():

    reader: ReaderAbstract = None
    readers = {
        'rss': RSSReader,
        'twitter': TwitterReader,
        'reddit': RedditReader,
        'basic-ad': BasicAdReader
    }

    def __init__(self, type: str) -> None:
        if type in self.readers.keys():
            self.reader = self.readers[type]()
        else:
            raise ReaderFactoryNotFoundException(
                type + " reader not found.")

        return
