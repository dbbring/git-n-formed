# Global Modules
import sys
import traceback
from multiprocessing import Process, Manager
# Custom Modules
from classes.feed_item import FeedItem
from classes.discord_helpers.discord_api_client import DiscordAPIClient
from classes.exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper


def process_feed(feed: dict, err_list: list):
    try:
        feed_item = FeedItem(feed)
        feed_item.get_feed().save()
        return
    except Exception as e:
        tracebk = sys.exc_info()
        err = CustomExceptionWrapper()
        err.orig_exception = e.with_traceback(tracebk[2])
        err.func_args['feed'] = feed
        err.stack_trace = "Stack Trace:\n{}".format(
            "".join(traceback.format_exception(type(e), e, e.__traceback__)))

        err_list.append(err)
        return


def main(feeds: dict, debug: bool = False):
    discord_api = DiscordAPIClient()
    feed_errors = ObjectListCustomExceptionWrapper('feed_errors')
    processes = []

    with Manager() as manager:
        links = discord_api.get_existing_links()
        feed_errors.custom_exceptions = manager.list([])

        for feed in feeds['feeds']:
            feed['existing_links'] = links
            ad = None

            ad_idx = int(feed['ad_index'])
            if ad_idx:
                ad = feeds['ads'][ad_idx - 1]  # Ad index is 1 based
                ad['existing_links'] = {}
                ad['channels'] = feed['channels']

            feed['ad'] = ad

            p = Process(target=process_feed, args=(
                feed, feed_errors.custom_exceptions))
            p.start()

            if debug:
                p.join()
            else:
                processes.append(p)

        for proc in processes:
            proc.join()

        feed_errors.save()
    return
