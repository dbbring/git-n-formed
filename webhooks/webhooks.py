# Global Modules
import argparse
import os
import sys
import traceback
from dotenv import load_dotenv
from honeybadger import honeybadger
# Custom Modules
from classes.main import Main
from classes.exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper


# ======================================================================
env_help_msg = "--env: Specifies the current running environment, either staging or prod."
debug_help_msg = "--debug: Runs processes on single core. Only logs to file and doesn't send checkin requests to honeybadger."
mp_help_msg = "--mp: Enables multiprocessing. Default is single process. Debug flag overrides MP."


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--env", help=env_help_msg, type=str, dest='env')
    parser.add_argument("--debug", help=debug_help_msg,
                        action='store_true', dest='debug')
    parser.add_argument("--mp", help=mp_help_msg,
                        action='store_true', dest='mp')
    args = parser.parse_args()

    curr_path = os.path.dirname(__file__)
    main_err_log = os.path.join(curr_path, 'main_errors.log')
    feed_err_path = os.path.join(curr_path, 'feed_errors.log')
    main_errors = ObjectListCustomExceptionWrapper(main_err_log, args.debug)

    try:
        env_path = os.path.join(curr_path, args.env, '.env')
        feed_path = os.path.join(curr_path, args.env, 'feeds.json')

        load_dotenv(dotenv_path=env_path)
        honeybadger.configure(api_key=os.getenv('HONEYBADGER_API_TOKEN'))

        main = Main(feed_path, args.mp, args.debug)
        main.run(feed_err_path)
        main.finalize()
    except Exception as e:
        tracebk = sys.exc_info()
        err = CustomExceptionWrapper()
        err.orig_exception = e.with_traceback(tracebk[2])
        err.stack_trace = "Stack Trace:\n{}".format(
            "".join(traceback.format_exception(type(e), e, e.__traceback__)))

        main_errors.custom_exceptions.append(err)

    main_errors.save()
