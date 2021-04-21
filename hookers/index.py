# Global Modules
import json
import os
from dotenv import load_dotenv
# Custom Modules
from classes.feed_item import FeedItem
from classes.discord_helpers.discord_api_client import DiscordAPIClient

load_dotenv()
ad_counter = 0
discord_api = DiscordAPIClient()

with open(os.path.dirname(__file__) + '/feeds.json') as f:
    feeds = json.load(f)

# links = discord_api.get_existing_links()


def main(feed: dict, ad_index: int, exisiting_links: dict = {}):
    # feed_item = FeedItem(feed, links)
    feed_item = FeedItem(feed)
    feed_item.get_feed().save()

    if feed["display_ad"]:
        ad = feeds['ads'][ad_counter]

        ad_item = FeedItem(ad)
        ad_item.get_feed().save()
    return


for feed in feeds['feeds']:
    ad_counter = ad_counter + \
        1 if ad_counter < (len(feeds['ads']) - 1) else 0
    main(feed, ad_counter)
