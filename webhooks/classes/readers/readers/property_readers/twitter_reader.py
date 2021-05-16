# Global Modules
from __future__ import annotations
import os
import datetime
import tweepy
# Custom Modules
from ._property_reader_abstract import PropertyReaderAbstract
from ....post_items.items import PostItem
from ....utils.string_utils import StringUtils


class NotAuthenticatedTwitterExcpetion(Exception):
    pass


class TwitterReader(PropertyReaderAbstract):

    __api = None
    # List[Post_Items]
    post_items: filter = []
    # List[content_items] content items being whatever native structure the reader gets
    _content_list: list = []
    # Optionable args from feed json
    properties = {}

    def __init__(self) -> None:
        self.__authenticate()
        self._content_list = []
        self.post_items = []
        self.properties = {
            "allow_retweets": False,
            "max_search_tweets": 10
        }
        return

    def __authenticate(self) -> None:
        auth = tweepy.AppAuthHandler(
            os.getenv('TWITTER_API'), os.getenv('TWITTER_API_SECRET'))
        self.__api = tweepy.API(auth)

        if self.__api == None:
            raise NotAuthenticatedTwitterExcpetion(
                "We could not OAuth2 with Twitter.")

        return

    def __is_current_tweet(self, tweet) -> bool:
        # Just case our time zones are mixed, checked for posts the next day 
        today = datetime.date.today()
        tomarrow = today + datetime.timedelta(days=1)
        post_date = tweet.created_at.date()

        if today == post_date or tomarrow == post_date:
            return True

        return False

    def __get_latest_content(self) -> None:
        for tweet in self._content_list:
            if self.__is_current_tweet(tweet):
                self.post_items.append(
                    self._to_post_item(tweet))
        return

    def __parse_content(self) -> None:
        self.__get_latest_content()
        self.post_items = filter(self._is_valid_link, self.post_items)
        return None

    def _is_valid_link(self, post_item: PostItem) -> bool:
        if post_item.link == '':
            return False

        if StringUtils.extract_url(post_item.link) == '':
            return False

        return True

    def _to_post_item(self, tweet) -> PostItem:
        return PostItem(
            content='', link='https://twitter.com/i/web/status/' + tweet.id_str)

    def fetch(self, url: str) -> TwitterReader:
        extra_params = "+exclude:replies+exclude:retweets"
        self._content_list = tweepy.Cursor(
            self.__api.search, q=url + extra_params).items(self.properties["max_search_tweets"])
        self.__parse_content()
        return self
