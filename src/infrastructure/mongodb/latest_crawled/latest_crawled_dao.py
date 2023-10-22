from typing import Optional

from injector import inject
from pymongo.collection import Collection
from pymongo.database import Database

from src.infrastructure.mongodb.latest_crawled.latest_crawled_dto import (
    LatestCrawledDto,
)


class LatestCrawledDao:
    @inject
    def __init__(self, db: Database):
        self._collection: Collection = db["tw_latest_crawled"]

    def read(self) -> Optional[LatestCrawledDto]:
        return self._collection.find_one()

    def update(self, dto: LatestCrawledDto):
        self._collection.update_one(
            {'_id': dto["_id"]}, {'$set': {"value": dto["value"]}}
        )
