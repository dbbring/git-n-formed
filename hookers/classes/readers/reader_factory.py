from .reader_abstract import ReaderAbstract
from .rss_reader import RSSReader
from .twitter_reader import TwitterReader
from .reddit_reader import RedditReader


class FactoryReaderNotFoundException(Exception):
    pass


class ReaderFactory():

    reader: ReaderAbstract = None
    readers = {
        'rss': RSSReader,
        'twitter': TwitterReader,
        'reddit': RedditReader
    }   

    def __init__(self, type: str):
        try:
            self.reader = self.readers[type]()
        except KeyError:
            raise FactoryReaderNotFoundException(
                type + " reader not found.")

        return
