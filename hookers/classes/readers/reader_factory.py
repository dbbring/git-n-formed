from .reader_abstract import ReaderAbstract
from .rss_reader import RSSReader


class FactoryReaderNotFoundException(Exception):
    pass


class ReaderFactory():

    reader: ReaderAbstract = None
    readers = {
        'rss': RSSReader
    }

    def __init__(self, type: str):
        try:
            self.reader = self.readers[type]()
        except KeyError:
            raise FactoryReaderNotFoundException(
                type + " reader not found.")

        return
