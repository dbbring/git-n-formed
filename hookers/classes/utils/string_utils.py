import re


class StringUtils(object):

    @staticmethod
    def sanitize_url(dirty_url: str) -> str:
        if len(dirty_url) == 0:
            return ''

        clean_url = dirty_url.replace('https', '')
        clean_url = clean_url.replace('http', '')
        clean_url = clean_url.replace('://www.', '')
        clean_url = clean_url.replace('://', '')

        if clean_url[len(clean_url) - 1] == '/':
            clean_url = clean_url[0:len(clean_url) - 1]

        return clean_url

    @staticmethod
    def extract_url(string: str) -> str:
        pattern = re.compile(
            r"(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?")
        result = pattern.search(string)

        if result == None:
            return ''

        return result.group(0)

    @staticmethod
    def extract_date(string: str) -> str:
        pattern = re.compile(
            r"\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])*")
        result = pattern.search(string)

        if result == None:
            return ''

        return result.group(0)
