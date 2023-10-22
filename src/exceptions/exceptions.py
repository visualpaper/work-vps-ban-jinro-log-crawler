from typing import Optional

from src.logcode import LogCode


class BanJinroLogCrawlerException(Exception):
    def __init__(self, log_code: LogCode, message: Optional[str]):
        super().__init__(message)
        self._log_code = log_code

    @property
    def log_code(self) -> LogCode:
        return self._log_code


class IllegalArgumentsException(BanJinroLogCrawlerException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(LogCode.ILLEGAL_ARGUMENTS, message)


class IllegalStateException(BanJinroLogCrawlerException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(LogCode.ILLEGAL_STATE, message)


class LatestCrawledReadWriteException(BanJinroLogCrawlerException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(LogCode.LATEST_CRAWLED_ERROR, message)


class VillageReadWriteException(BanJinroLogCrawlerException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(LogCode.VILLAGE_ERROR, message)


class ParserException(BanJinroLogCrawlerException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(LogCode.PARSER_ERROR, message)


class ApiRequestException(BanJinroLogCrawlerException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(LogCode.API_ERROR, message)
