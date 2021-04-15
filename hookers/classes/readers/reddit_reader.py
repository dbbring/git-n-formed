# Global Modules
import praw
import os
from dotenv import load_dotenv
# Custom Modules
from .reader_abstract import ReaderAbstract
class NotAuthenticatedRedditExcpetion(Exception):
    pass


class RedditReader(ReaderAbstract):

    __reddit_api = None
    post_items = []
    
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.__reddit_api = praw.Reddit(
            client_id=os.getenv('REDDIT_API'),
            client_secret=os.getenv('REDDIT_API_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        return

    def _to_post_item(self, tweet):
        return PostItem()

    def fetch(self, url:str):
        subreddit = self.__reddit_api.subreddit(url)
        for sub in subreddit.new(limit=10):
            # check ups for up votes remove spam
            # check content for urls maybe we have already hit up a link to that
            print(sub.title)
        return
