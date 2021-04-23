# Global Modules
import json
import os
import sys
from dotenv import load_dotenv
from multiprocessing import Process, Manager
import traceback
# Custom Modules
from classes.feed_item import FeedItem
from classes.discord_helpers.discord_api_client import DiscordAPIClient
from classes.exception_helpers.exception_wrapper import CustomException, ExceptionWrapper

# ======================================================================


def main(feed: dict, ad: dict, err_list: list, exisiting_links: dict = {}):
    try:
        feed_item = FeedItem(feed, exisiting_links)
        feed_item.get_feed().save()

        if feed["display_ad"]:
            ad_item = FeedItem(ad)
            ad_item.get_feed().save()
        return
    except Exception as e:
        tb = sys.exc_info()
        err = CustomException()
        err.orig_exception = e.with_traceback(tb[2])
        err.func_args['ad'] = ad
        err.func_args['feed'] = feed
        err.func_args['exist-links'] = exisiting_links
        err.stack_trace = "Stack Trace:\n{}".format(
            "".join(traceback.format_exception(type(e), e, e.__traceback__)))

        err_list.append(err)
        return


# ======================================================================


if __name__ == '__main__':

    main_errors = ExceptionWrapper('main_errors')
    try:
        load_dotenv()
        ad_counter = -1
        discord_api = DiscordAPIClient()
        errors = ExceptionWrapper('feed_errors')

        with open(os.path.dirname(__file__) + '/feeds.json') as f:
            feeds = json.load(f)

        links = discord_api.get_existing_links()

        with Manager() as manager:
            errors.custom_exceptions = manager.list([])

            for feed in feeds['feeds']:
                ad_counter = ad_counter + \
                    1 if ad_counter < (len(feeds['ads']) - 1) else -1
                ad = feeds['ads'][ad_counter]

                p = Process(target=main, args=(
                    feed, ad, errors.custom_exceptions, links))
                p.start()
                p.join()

            errors.save()

    except Exception as e:
        tb = sys.exc_info()
        err = CustomException()
        err.orig_exception = e.with_traceback(tb[2])
        err.stack_trace = "Stack Trace:\n{}".format(
            "".join(traceback.format_exception(type(e), e, e.__traceback__)))

        main_errors.custom_exceptions.append(err)

    main_errors.save()
