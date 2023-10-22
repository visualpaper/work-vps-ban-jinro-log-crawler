from src.config.logger import get_logger
from src.exceptions.exceptions import BanJinroLogCrawlerException
from src.logcode import LogCode

logger = get_logger()


# Application 例外ハンドラ
def application_exception_handler(exc: BanJinroLogCrawlerException) -> None:
    _do_logging(exc.log_code, exc)


# BaseException 例外ハンドラ
def base_exception_handler(exc: Exception) -> None:
    _do_logging(LogCode.UNEXPECTED, exc)


def _do_logging(log_code: LogCode, exc: Exception) -> None:
    logger.log(
        level=log_code.log_level,
        msg="{} {}".format(log_code.code, log_code.message),
    )
    logger.info("exc", exc_info=exc)
