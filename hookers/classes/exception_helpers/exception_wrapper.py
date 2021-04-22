import os
import datetime
import traceback


class CustomException(Exception):

    orig_exception: Exception = None
    func_args: dict = {}
    stack_trace: str = ''

    def __init__(self) -> None:
        super().__init__()
        self.orig_exception = None
        self.func_args = {}
        self.stack_trace = ''

    def format_orig_exception(self) -> str:
        result = ''
        for arg in self.func_args.keys():
            result += arg + ' = ' + str(self.func_args[arg]) + '\n'
        return result

    def format_func_args(self) -> str:
        result = ''
        result += '{}'.format(self.orig_exception)
        result += '\n\n'
        result += self.stack_trace

        return result


class ExceptionWrapper(object):

    __log_file: str = ''
    custom_exceptions: list = []  # List of CustomExceptions

    def __init__(self, full_log_name:str) -> None:
        super().__init__()
        self.__log_file = os.getcwd() + full_log_name
        return

    def __format_for_log(self, custom_ex: CustomException) -> str:
        result = '\n'
        result += datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + '\n'
        result += custom_ex.format_orig_exception()
        result += '\n'
        result += custom_ex.format_func_args()
        result += '\n'
        return result

    def save(self):
        with open(self.__log_file, 'a+') as f:
            for ex in self.custom_exceptions:
                f.write(self.__format_for_log(ex))
        return
