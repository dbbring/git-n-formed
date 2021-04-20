# Global Modules
import json
import os
from dotenv import load_dotenv
# Custom Modules
from classes.feed_item import FeedItem
from classes.discord_helpers.discord_api_client import DiscordAPIClient


load_dotenv()
# discord_api = DiscordAPIClient()
# links = discord_api.get_existing_links()

with open(os.path.dirname(__file__) + '/feeds.json') as f:
    feeds = json.load(f)

for feed in feeds['feeds']:
    feeditem = FeedItem(feed)
    feeditem.get_feed().save()
