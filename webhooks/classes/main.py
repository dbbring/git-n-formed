# Global Modules
import json
import honeybadger
import requests
import sys
import traceback
import os
from multiprocessing import Process, Manager, Queue
# Custom Modules
from .discord_helpers.discord_api_client import DiscordAPIClient
from .exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper
from .feed_items.feed_item import FeedItem
from .discord_helpers.discord_webhook import DiscordRoutes
from .utils.int_utils import IntUtils


class Main():
    NUMBER_OF_SHUFFLES = 5
    __existing_links: dict = {}
    __debug: bool = False
    __mp: bool = False
    __msgs: list = []
    feeds: dict = {}

    def __init__(self, feed_path: str, enable_mp: bool = False, debug: bool = False) -> None:
        discord_api = DiscordAPIClient()

        self.__debug = debug
        self.__mp = enable_mp
        self.__msgs = []
        self.feeds = {}
        self.__existing_links = discord_api.get_existing_links()
        with open(feed_path) as f:
            self.feeds = json.load(f)
        return

    def __honeybadger_check_in(self, url: str) -> None:
        r = requests.get(url)

        if r.status_code != 200:
            honeybadger.notify(
                f'Honeybadger check-in failed with status code: {r.status_code}')
        return None

    def __filter_msgs_by_chan(self, channel: str, all_msgs: list) -> list:
        chan_msgs = []
        for msg in all_msgs:
            if channel == msg.channel:
                chan_msgs.append(msg)
        return chan_msgs

    def post_by_channel(self, channel: str, all_msgs: list, num_of_shuffles: int) -> None:
        chan_msgs = self.__filter_msgs_by_chan(channel, all_msgs)
        indexes = IntUtils.random_list(len(chan_msgs), num_of_shuffles)

        if len(chan_msgs) == 0:
            return None

        for index in indexes:
            chan_msgs[index].post()

        return None

    def __finalize_mp(self, channels: list) -> None:
        processes = []

        for channel in channels:
            proc = Process(target=self.post_by_channel, args=(
                channel, self.__msgs, self.NUMBER_OF_SHUFFLES))
            proc.start()
            processes.append(proc)

        for proc in processes:
            proc.join()

        return None

    def finalize(self):
        channels = DiscordRoutes().get_all_channels()

        if self.__mp and not self.__debug:
            self.__finalize_mp(channels)
        else:
            for channel in channels:
                self.post_by_channel(channel, self.__msgs,
                                     self.NUMBER_OF_SHUFFLES)

        if not self.__debug:
            self.__honeybadger_check_in(
                os.getenv('HONERYBADGER_END_SCRIPT_URL'))

        return None

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

    def __run_mp(self, results: Queue, err_list: ObjectListCustomExceptionWrapper) -> None:
        processes = []

        with Manager() as manager:
            err_list.custom_exceptions = manager.list([])

            for feed in self.feeds['feeds']:
                complete_feed = self.setup_feed(feed, self.feeds['ads'])

                p = Process(target=self.process_feed, args=(
                    complete_feed, results, err_list.custom_exceptions))
                p.start()
                processes.append(p)

            while results.qsize() != 0:
                self.__msgs += results.get()

            for p in processes:
                p.join()

            err_list.save()
        return

    def run(self, feed_err_path: str) -> None:
        feed_errors = ObjectListCustomExceptionWrapper(
            feed_err_path, self.__debug)
        results = Queue()

        if not self.__debug:
            self.__honeybadger_check_in(
                os.getenv('HONERYBADGER_START_SCRIPT_URL'))

        if self.__mp and not self.__debug:
            self.__run_mp(results, feed_errors)
            return None

        for feed in self.feeds['feeds']:
            complete_feed = self.setup_feed(feed, self.feeds['ads'])
            self.process_feed(
                complete_feed, results, feed_errors.custom_exceptions)

        while results.qsize() != 0:
            self.__msgs += results.get()

        feed_errors.save()
        return None
