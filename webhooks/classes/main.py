# Global Modules
import sys
import traceback
import random
from multiprocessing import Process, Manager, Queue
# Custom Modules
from .discord_helpers.discord_api_client import DiscordAPIClient
from .exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper
from .feed_items.feed_item import FeedItem
from .discord_helpers.discord_webhook import DiscordRoutes


class Main():
    __existing_links: dict = {}
    __debug: bool = False
    __final_msgs: list = []

    def __init__(self, debug: bool = False) -> None:
        discord_api = DiscordAPIClient()

        self.__debug = debug
        self.__final_msgs = []
        self.__existing_links = discord_api.get_existing_links()
        return

    def __shuffle_msgs_by_channel(self, dirty_msg_list: list) -> list:
        sorted_msgs = {}
        result = []
        channels = DiscordRoutes().get_all_channels()

        for channel in channels:
            sorted_msgs[channel] = []

        for msg in dirty_msg_list:
            sorted_msgs[msg.channel].append(msg)

        for channel in sorted_msgs.keys():
            random.shuffle(sorted_msgs[channel])
            result += sorted_msgs[channel]
        return result

    def process_feed(self, feed: dict, output_queue: Queue, err_list: list):
        try:
            msgs = []
            ad_msgs = []

            feed_item = FeedItem(feed)
            msgs = feed_item.get_feed().get_message_list()

            if feed['ad'] is not None and len(msgs) > 0:
                ad_item = FeedItem(feed['ad'])
                ad_msgs = ad_item.get_feed().get_message_list()
                msgs += ad_msgs

            if len(msgs) > 0:
                output_queue.put(msgs)
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

    def setup_feed(self, feed: dict, ads: list) -> dict:
        feed['existing_links'] = self.__existing_links
        ad = None

        ad_idx = int(feed['ad_index'])
        if ad_idx:
            ad = ads[ad_idx - 1]  # Ad index is 1 based
            ad['existing_links'] = {}
            ad['channels'] = feed['channels']
            ad['ad'] = None

        feed['ad'] = ad
        return feed

    def finalize(self):
        self.__final_msgs = self.__shuffle_msgs_by_channel(self.__final_msgs)
        for msg in self.__final_msgs:
            msg.post()
        return

    def run(self, feeds: dict):
        feed_errors = ObjectListCustomExceptionWrapper('feed_errors')
        results = Queue()
        processes = []

        with Manager() as manager:
            feed_errors.custom_exceptions = manager.list([])

            for feed in feeds['feeds']:
                complete_feed = self.setup_feed(feed, feeds['ads'])

                if self.__debug:
                    self.process_feed(
                        complete_feed, results, feed_errors.custom_exceptions)
                else:
                    p = Process(target=self.process_feed, args=(
                        complete_feed, results, feed_errors.custom_exceptions))
                    p.start()
                    processes.append(p)

            while results.qsize() != 0:
                self.__final_msgs += results.get()

            for p in processes:
                p.join()

            feed_errors.save()
        return
