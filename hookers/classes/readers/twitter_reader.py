
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

    __api = None
    # List[Post_Items]
    post_items = []

    def __init__(self):
        load_dotenv()
        self.__authenticate()
        return

    def __authenticate(self):
        auth = tweepy.OAuthHandler(os.getenv('TWITTER_API'), os.getenv('TWITTER_API_SECRET'))
        auth.set_access_token(access_token, access_token_secret)
        self.__api = tweepy.API(auth)

        if self.__api == None:
            raise NotAuthenticatedTwitterExcpetion("We could not OAuth with Twitter.")


    def fetch(self):
        public_tweets = api.home_timeline()

        for tweet in public_tweets:
            print(tweet.text)

    def _to_post_item(self):
        return

    