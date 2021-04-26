# Global Modules
import json
import os
import sys
import traceback
# Custom Modules
from main import main
from classes.exception_helpers.custom_exception_wrapper import CustomExceptionWrapper, ObjectListCustomExceptionWrapper


# ======================================================================


if __name__ == '__main__':

    main_errors = ObjectListCustomExceptionWrapper('main_errors')

    try:
        with open(os.path.dirname(__file__) + '/feeds.json') as f:
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
