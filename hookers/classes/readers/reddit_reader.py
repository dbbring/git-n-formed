# Global Modules

# Custom Modules
from .reader_abstract import ReaderAbstract


class NotAuthenticatedRedditExcpetion(Exception):
    pass


class RedditReader(ReaderAbstract):
    pass
