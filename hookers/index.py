# Global Modules
import json
import os
from dotenv import load_dotenv
# Custom Modules
from classes.feed_item import FeedItem
from classes.discord_helpers.discord_api import DiscordAPI


load_dotenv()


with open(os.path.dirname(__file__) + '/config.json') as f:
    config = json.load(f)

# ============= TODO ================================
# get a list of links to see if we already posted it
# only need one list then reference that depends on the
# channel, maybe setup a dict<channel, list> ? globals not thread safe

# use enum and every so often insert banner ads for supporter
# or other companies / only in free chans, maybe divide total feeds
# to see how many times we need to show it

for feed in config['feeds']:
    # spin off new thread eventually
    # try catch, on error log it so we can inspect the feed manually
    feeditem = FeedItem(feed)
    feeditem.get_feed().save()
