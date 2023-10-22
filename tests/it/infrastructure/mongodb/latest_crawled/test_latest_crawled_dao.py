from typing import Optional

import mongomock
import pytest
from pymongo.collection import Collection

from src.infrastructure.mongodb.latest_crawled.latest_crawled_dao import (
    LatestCrawledDao,
)
from src.infrastructure.mongodb.latest_crawled.latest_crawled_dto import (
    LatestCrawledDto,
)


class TestLatestCrawledDao:
    _dao: LatestCrawledDao
    _collection: Collection

    @pytest.fixture(autouse=True)
    def fixture(self):
        client = mongomock.MongoClient()
        db = client["db"]
        self._dao = LatestCrawledDao(db)
        self._collection = client["db"]["tw_latest_crawled"]
        yield
        client.drop_database("db")

    def test_not_exists(self):
        dto: Optional[LatestCrawledDto] = self._dao.read()

        assert dto is None

    def test_normal(self):
        to_insert = [
            {"value": 1},
        ]
        self._collection.insert_many(to_insert)
        dto: Optional[LatestCrawledDto] = self._dao.read()

        assert dto is not None
        assert dto["value"] == 1

        dto["value"] = 2
        self._dao.update(dto)
        dto_after: Optional[LatestCrawledDto] = self._dao.read()

        assert dto_after is not None
        assert dto_after["value"] == 2
