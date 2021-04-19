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

with open(os.path.dirname(__file__) + '/config.json') as f:
    config = json.load(f)

# ============= TODO ================================
# get a list of links to see if we already posted it
# only need one list then reference that depends on the
# channel, maybe setup a dict<channel, list> ? globals not thread safe
# list needs to be a set and use the in

# use enum and every so often insert banner ads for supporter
# or other companies / only in free chans, maybe divide total feeds
# to see how many times we need to show it

# break config into seperate readers then send each off with its own process

for feed in config['feeds']:
    feeditem = FeedItem(feed)
    feeditem.get_feed().save()
