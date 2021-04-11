
# Global Modules
import os
import tweepy
from dotenv import load_dotenv
# Custom Modules
from .reader_abstract import ReaderAbstract
from ..post_items.post_item import PostItem

class NotAuthenticatedTwitterExcpetion(Exception):
    pass

class TwitterReader(ReaderAbstract):

    MAX_SEARCH_TWEETS = 200
    __api = None
    # List[Post_Items]
    post_items = []
    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []

    def __init__(self):
        load_dotenv()
        self.__authenticate()
        self._content_list = []
        return

    def __authenticate(self):
        auth = tweepy.AppAuthHandler(os.getenv('TWITTER_API'), os.getenv('TWITTER_API_SECRET'))
        self.__api = tweepy.API(auth)

        if self.__api == None:
            raise NotAuthenticatedTwitterExcpetion("We could not OAuth with Twitter.")


    def fetch(self, url:str):
        # gonna have to use id coupled with web/i/<id> for the twitter link at the end
        # then just use the text attribute, maybe strip out all https? 
        for tweet in tweepy.Cursor(self.__api.search, q=url).items(self.MAX_SEARCH_TWEETS):
            print(tweet.text)

    def _to_post_item(self):
        return

    