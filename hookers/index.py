# Global Modules
import json
import os
from dotenv import load_dotenv
# Custom Modules
from classes.feed_item import FeedItem


load_dotenv()

with open(os.path.dirname(__file__) + '/config.json') as f:
    config = json.load(f)

# ============= TODO ================================
# get a list of links to see if we already posted it
# only need one list then reference that

# create .env file for api keys

for feed in config['feeds']:
    # spin off new thread eventually
    #feeditem = FeedItem(feed)
    #feeditem.get_feed().save()
