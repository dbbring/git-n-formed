# Global Modules
import os
import datetime
import tweepy
from dotenv import load_dotenv
# Custom Modules
from .reader_abstract import ReaderAbstract
from ..post_items.post_item import PostItem


class NotAuthenticatedTwitterExcpetion(Exception):
    pass


class TwitterReader(ReaderAbstract):

    MAX_SEARCH_TWEETS = 25
    __api = None
    # List[Post_Items]
    post_items = []
    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []
    properties = {}

    def __init__(self):
        load_dotenv()
        self.__authenticate()
        self._content_list = []
        return

    def __authenticate(self):
        try:
            auth = tweepy.AppAuthHandler(
                os.getenv('TWITTER_API'), os.getenv('TWITTER_API_SECRET'))
            self.__api = tweepy.API(auth)

            if self.__api == None:
                raise Exception
        except:
            raise NotAuthenticatedTwitterExcpetion(
                "We could not OAuth2 with Twitter.")

    def __is_current_tweet(self, tweet) -> bool:
        today = datetime.date.today()
        post_date = tweet.created_at.date()

        if today == post_date:
            return True

        return False

    def __is_not_retweet(self, tweet) -> bool:
        try:
            tweet.retweeted_status.text
            return False
        except AttributeError:  # Not a Retweet
            return True

    def __get_latest_content(self) -> None:
        for tweet in self._content_list:
            if self.__is_current_tweet(tweet) and self.__is_not_retweet(tweet):
                self.post_items.append(
                    self._to_post_item(tweet))
        return

    def __process_content(self) -> None:
        self.__get_latest_content()
        for index, post in enumerate(self.post_items):
            if self._is_valid_link(post.link) == False:
                self.post_items.pop(index)
        return None

    def _is_valid_link(self, link: str) -> bool:

        # additional checks here like already posted in chan

        if link == '':
            return False

        return True

    def _to_post_item(self, tweet):
        return PostItem(
            content='', link='https://twitter.com/i/web/status/' + tweet.id_str)

    def fetch(self, url: str):
        self._content_list = tweepy.Cursor(
            self.__api.search, q=url).items(self.MAX_SEARCH_TWEETS)
        self.__process_content()
        return self
