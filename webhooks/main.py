# Global Modules
import sys
import traceback
from dotenv import load_dotenv
from multiprocessing import Process, Manager
# Custom Modules
from classes.feed_item import FeedItem
from classes.discord_helpers.discord_api_client import DiscordAPIClient
from classes.exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper


def process_feed(feed: dict, ad: dict, err_list: list, exisiting_links: dict = {}):
    try:
        feed_item = FeedItem(feed, exisiting_links)
        feed_item.get_feed().save()

        if feed["display_ad"]:
            ad_item = FeedItem(ad)
            ad_item.get_feed().save()
        return
    except Exception as e:
        tracebk = sys.exc_info()
        err = CustomExceptionWrapper()
        err.orig_exception = e.with_traceback(tracebk[2])
        err.func_args['ad'] = ad
        err.func_args['feed'] = feed
        err.func_args['exist-links'] = exisiting_links
        err.stack_trace = "Stack Trace:\n{}".format(
            "".join(traceback.format_exception(type(e), e, e.__traceback__)))

        err_list.append(err)
        return


def main(feeds: dict):
    load_dotenv(dotenv_path="./webhooks/staging/.env")
    ad_counter = -1
    discord_api = DiscordAPIClient()
    feed_errors = ObjectListCustomExceptionWrapper('feed_errors')

    with Manager() as manager:
        links = discord_api.get_existing_links()
        feed_errors.custom_exceptions = manager.list([])

        for feed in feeds['feeds']:
            ad_counter = ad_counter + \
                1 if ad_counter < (len(feeds['ads']) - 1) else -1
            ad = feeds['ads'][ad_counter]

            p = Process(target=process_feed, args=(
                feed, ad, feed_errors.custom_exceptions, links))
            p.start()
            p.join()

        feed_errors.save()
    return
