# Global Modules
import argparse
import json
import os
import sys
import traceback
from dotenv import load_dotenv
# Custom Modules
from main import main
from classes.exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper


# ======================================================================
help_msg = "--env specifies the current running environment, either staging or prod."

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--env", help="", type=str)
    args = parser.parse_args()

    main_errors = ObjectListCustomExceptionWrapper('main_errors')

    try:
        load_dotenv(dotenv_path=os.path.dirname(
            __file__) + '/' + args.env + "/.env")
        with open(os.path.dirname(__file__) + '/' + args.env + '/feeds.json') as f:
            feeds = json.load(f)

        main(feeds)
    except Exception as e:
        tracebk = sys.exc_info()
        err = CustomExceptionWrapper()
        err.orig_exception = e.with_traceback(tracebk[2])
        err.stack_trace = "Stack Trace:\n{}".format(
            "".join(traceback.format_exception(type(e), e, e.__traceback__)))

        main_errors.custom_exceptions.append(err)

    main_errors.save()
