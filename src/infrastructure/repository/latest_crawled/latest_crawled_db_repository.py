from typing import Optional

from injector import inject

from src.domain.latest_crawled.latest_crawled_repository import LatestCrawledRepository
from src.exceptions.exceptions import LatestCrawledReadWriteException
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dao import (
    LatestCrawledDao,
)
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dto import (
    LatestCrawledDto,
)


class LatestCrawledDbRepository(LatestCrawledRepository):
    @inject
    def __init__(self, dao: LatestCrawledDao):
        self._dao = dao

    def read(self) -> int:
        dto: Optional[LatestCrawledDto] = self._dao.read()
        if dto is None:
            raise LatestCrawledReadWriteException()

        return dto["value"]

    def update(self, value: int) -> None:
        dto: Optional[LatestCrawledDto] = self._dao.read()
        if dto is None:
            raise LatestCrawledReadWriteException()

        dto["value"] = value
        self._dao.update(dto)
