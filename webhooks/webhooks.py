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
from classes.argparse_helpers.custom_argparse_wrapper import ArgparseWrapper


# ======================================================================


if __name__ == '__main__':
    try:
        curr_path = os.path.dirname(__file__)

        args = ArgparseWrapper(curr_path)
        args = args.get_args()

        main_err_log = os.path.join(curr_path, 'main_errors.log')
        feed_err_path = os.path.join(curr_path, 'feed_errors.log')
        env_path = os.path.join(curr_path, args.env, '.env')
        feed_path = os.path.join(curr_path, args.env, 'feeds.json')

        main_errors = ObjectListCustomExceptionWrapper(
            main_err_log, args.debug)

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
