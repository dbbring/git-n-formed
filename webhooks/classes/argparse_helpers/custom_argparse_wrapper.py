# Global Modules
import argparse
import os
# Custom Modules


class InvalidEnvironmentException(Exception):
    pass


class ArgparseWrapper(object):

    ENV_HELP_MSG = "--env: Specifies the current running environment, either staging or prod. Looks in CWD for folders containing .env and feeds.json files."
    DEBUG_HELP_MSG = "--debug: Runs processes on single core. Only logs to file and doesn't send check-in requests to HoneyBadger."
    MP_HELP_MSG = "--mp: Enables multiprocessing. Default is single process. Debug flag overrides MP."
    parser: argparse.ArgumentParser = None
    cwd: str = ''

    def __init__(self, curr_file_path: str = '') -> None:
        super().__init__()
        self.parser = argparse.ArgumentParser()
        self.cwd = curr_file_path
        self.set_args()
        return None

    def set_args(self) -> None:
        self.parser.add_argument(
            "--env", help=self.ENV_HELP_MSG, type=str)
        self.parser.add_argument("--debug", help=self.DEBUG_HELP_MSG,
                                 action='store_true')
        self.parser.add_argument("--mp", help=self.MP_HELP_MSG,
                                 action='store_true')
        return None

    def get_args(self):
        args = self.parser.parse_args()

        if args.env == '':
            raise InvalidEnvironmentException(
                'You must specify a environment!')

        if not os.path.isdir(os.path.join(self.cwd, args.env)):
            raise InvalidEnvironmentException(
                'Invalid Enviroment. No environment folder found!')

        return args
