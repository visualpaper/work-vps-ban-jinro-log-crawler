import logging
from enum import Enum


class CaseCode(Enum):
    BASE = "BASE"
    APP = "APPL"
    STORAGE = "STRG"
    API = "_API"
    OTHER = "OTHE"


class LogCode(Enum):
    # Common Related LogCode.
    UNEXPECTED = (CaseCode.BASE, 0, logging.ERROR, "Unexpected Error")
    ILLEGAL_ARGUMENTS = (CaseCode.BASE, 1, logging.ERROR, "Illegal Arguments")
    ILLEGAL_STATE = (CaseCode.BASE, 2, logging.ERROR, "Illegal State")
    IO_ERROR = (CaseCode.BASE, 3, logging.ERROR, "IO Error")

    # Application Related LogCoce.
    LATEST_CRAWLED_ERROR = (
        CaseCode.APP,
        0,
        logging.WARN,
        "Latest Crawled Read/Write Error",
    )

    VILLAGE_ERROR = (
        CaseCode.APP,
        1,
        logging.WARN,
        "village Read/Write Error",
    )

    # Storage Related LogCode.
    STORAGE_UNEXPECTED = (
        CaseCode.STORAGE,
        0,
        logging.WARN,
        "Storage Unexpected Error",
    )

    # Api Related LogCode.
    API_ERROR = (
        CaseCode.API,
        0,
        logging.WARN,
        "API Error",
    )

    # other Related LogCode
    PARSER_ERROR = (
        CaseCode.OTHER,
        0,
        logging.ERROR,
        "API Error",
    )

    def __init__(
        self, case_code: CaseCode, detail_code: int, log_level: int, message: str
    ):
        self._case_code = case_code
        self._detail_code = detail_code
        self._log_level = log_level
        self._message = message

    @property
    def code(self) -> str:
        return "{}-{}".format(self._case_code.value, str(self._detail_code).zfill(4))

    @property
    def log_level(self) -> int:
        return self._log_level

    @property
    def message(self) -> str:
        return self._message
