# Global Modules
import os
import datetime
# Custom Modules


class CustomExceptionWrapper(Exception):

    orig_exception: Exception = None
    func_args: dict = {}
    stack_trace: str = ''

    def __init__(self) -> None:
        super().__init__()
        self.orig_exception = None
        self.func_args = {}
        self.stack_trace = ''
        return

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

    def format_for_log(self) -> str:
        result = '\n'
        result += datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + '\n'
        result += self.format_orig_exception()
        result += '\n'
        result += self.format_func_args()
        result += '\n'
        return result


class ObjectListCustomExceptionWrapper(object):

    __log_file: str = ''
    custom_exceptions: list = []  # List of CustomExceptionWrapper

    def __init__(self, log_name: str) -> None:
        super().__init__()
        self.custom_exceptions = []
        self.__log_file = os.getcwd() + '\\' + log_name + '.log'
        return

    def save(self) -> None:
        if len(self.custom_exceptions) > 0:
            with open(self.__log_file, 'a+') as f:
                for custom_except in self.custom_exceptions:
                    f.write(custom_except.format_for_log())
        return
