from typing import List

from injector import inject
from pymongo.collection import Collection
from pymongo.database import Database

from src.infrastructure.mongodb.village.village_dto import VillageDto


class VillageDao:
    @inject
    def __init__(self, db: Database):
        self._collection: Collection = db["td_village"]

    def insertAll(self, dtos: List[VillageDto]) -> None:
        self._collection.insert_many(dtos)
